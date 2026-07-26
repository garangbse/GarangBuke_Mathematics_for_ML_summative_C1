"""
prediction.py

The API entrypoint required by the rubric's folder structure:
    summative/API/prediction.py

Contains ONLY: FastAPI routes, CORS config, and artifact loading.
All cleaning/encoding logic lives in preprocessing.py (imported below) --
the same file the Colab notebook uses -- so nothing here is a re-typed
copy of notebook logic. All training logic lives in training.py, used
only by /retrain.

Run locally:    uv run uvicorn prediction:app --reload
Swagger UI:     http://127.0.0.1:8000/docs
"""

import io
import joblib
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from schemas import PredictionRequest, PredictionResponse, RetrainResponse, HealthResponse
from preprocessing import build_single_record_row
from training import (
    train_and_select_best,
    MODEL_PATH, SCALER_PATH, FEATURE_COLUMNS_PATH, COLUMNS_TO_SCALE_PATH,
    TRAIN_MEDIANS_PATH, METADATA_PATH,
)
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TRAINING_DATA_PATH = os.path.join(DATA_DIR, "training_data.csv")

app = FastAPI(
    title="Freelancer Hourly Rate Prediction API",
    description="Predicts a freelancer's hourly rate (USD) from profile attributes, "
                "and supports on-demand retraining when new data becomes available.",
    version="1.0.0",
)


# CORS -- explicit allow-list, not a wildcard. See README for full reasoning.

# ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost:\d+",
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

_artifacts = {}


def _load_artifacts():
    return {
        "model": joblib.load(MODEL_PATH),
        "scaler": joblib.load(SCALER_PATH),
        "feature_cols": joblib.load(FEATURE_COLUMNS_PATH),
        "cols_to_scale": joblib.load(COLUMNS_TO_SCALE_PATH),
        "train_medians": joblib.load(TRAIN_MEDIANS_PATH),
        "metadata": joblib.load(METADATA_PATH) if os.path.exists(METADATA_PATH) else {},
    }


@app.on_event("startup")
def _startup():
    global _artifacts
    _artifacts = _load_artifacts()


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health", response_model=HealthResponse, tags=["Monitoring"])
def health():
    return HealthResponse(
        status="ok",
        model_loaded=bool(_artifacts.get("model") is not None),
        best_model_name=_artifacts.get("metadata", {}).get("best_model_name"),
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(payload: PredictionRequest):
    if not _artifacts:
        raise HTTPException(status_code=503, detail="Model not loaded yet.")

    record = payload.model_dump()
    row = build_single_record_row(record, _artifacts["feature_cols"], _artifacts["train_medians"])

    row_df = pd.DataFrame([row])[_artifacts["feature_cols"]]
    row_df[_artifacts["cols_to_scale"]] = _artifacts["scaler"].transform(row_df[_artifacts["cols_to_scale"]])

    prediction = float(_artifacts["model"].predict(row_df)[0])

    return PredictionResponse(
        predicted_hourly_rate_usd=round(prediction, 2),
        model_used=_artifacts.get("metadata", {}).get("best_model_name", "unknown"),
    )


@app.post("/retrain", response_model=RetrainResponse, tags=["Model Management"])
def retrain(file: UploadFile = File(..., description="CSV of new freelancer rows")):
    global _artifacts

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file.")

    try:
        new_data = pd.read_csv(io.BytesIO(file.file.read()))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {exc}")

    required_cols = {
        "freelancer_ID", "name", "gender", "age", "country", "language",
        "primary_skill", "years_of_experience", "hourly_rate (USD)", "rating",
        "is_active", "client_satisfaction",
    }
    missing = required_cols - set(new_data.columns)
    if missing:
        raise HTTPException(status_code=422, detail=f"Missing required columns: {sorted(missing)}")

    existing_data = pd.read_csv(TRAINING_DATA_PATH)
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    combined_data.to_csv(TRAINING_DATA_PATH, index=False)

    summary = train_and_select_best(combined_data)   # from training.py
    _artifacts = _load_artifacts()                    # hot-swap into memory

    return RetrainResponse(
        status="retrained_and_reloaded",
        best_model=summary["best_model"],
        n_training_rows=summary["n_training_rows"],
        all_model_metrics=summary["all_model_metrics"],
    )

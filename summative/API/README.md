# Freelancer Hourly Rate Prediction API

FastAPI service wrapping the Task 1 best-performing regression model.

## File overview
- `prediction.py` — the API itself: CORS, `/predict`, `/retrain`, `/health`, Swagger UI at `/docs`
- `preprocessing.py` — cleaning/feature-engineering functions (single source of truth, also used by the notebook)
- `training.py` — the 4-model training pipeline, used by `/retrain`
- `train_initial_model.py` — one-time script that populates `artifacts/`
- `artifacts/` — saved model + scaler + feature schema (already included, trained)
- `data/training_data.csv` — accumulated training data (base data + anything uploaded via `/retrain`)

---

## Part A — Run it locally with `uv`

### 1. Install uv (one-time)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install dependencies (from the `summative/` folder, one level up)
```bash
cd ..            # into summative/
uv sync
cd API
```

### 3. (Optional) Retrain the initial model — artifacts/ already ships trained
```bash
uv run --project .. python train_initial_model.py
```

### 4. Run the API
```bash
uv run --project .. uvicorn prediction:app --reload
```
- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

### 5. Try it
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "female", "age": 34, "country": "India",
    "primary_skill": "Machine Learning", "years_of_experience": 6,
    "rating": 4.2, "is_active": true, "client_satisfaction": 88.0
  }'
```

Retrain (upload a CSV of new rows, same columns as `global_freelancers_raw.csv`):
```bash
curl -X POST http://127.0.0.1:8000/retrain \
  -F "file=@path/to/new_freelancers.csv;type=text/csv"
```
Or use the Swagger UI at `/docs` → `POST /retrain` → "Try it out". The response reports which
of the 4 models won and its RMSE/R², and the server immediately starts using the new model.

---

## Part B — Deploy to Render

1. Push the whole repo to GitHub.
2. Render → **New +** → **Web Service** → connect the repo.
3. **Root Directory:** `linear_regression_model/summative/API`
4. **Build Command:**
   ```bash
   pip install uv && uv pip install --system -r requirements.txt
   ```
5. **Start Command:**
   ```bash
   uvicorn prediction:app --host 0.0.0.0 --port $PORT
   ```
6. Deploy. Your Swagger UI (the public link required by the rubric) will be:
   ```
   https://<your-service-name>.onrender.com/docs
   ```
   Paste this into the top-level `README.md`.

> Commit `artifacts/` and `data/` to git so the deployed service has a working model on first boot.

> **Free-tier note:** Render's free services sleep after inactivity and take ~30-50s to wake up on
> the next request — normal, not a bug.

---

## Design notes (mapped to rubric requirements)
- **POST `/predict`** — validated by `schemas.PredictionRequest` (Pydantic). Every field has an
  explicit type (`int`, `float`, `bool`, `Enum`) and a range/choice constraint. Bad input → automatic `422`.
- **CORS** — explicit allow-list (not `"*"`), `GET`/`POST` only, restricted headers,
  `allow_credentials=False`. Reasoning is written directly above `app.add_middleware(...)` in `prediction.py`.
- **Retraining** — `POST /retrain` is a live, reactive endpoint: upload a CSV → appended to the
  training set → all 4 models retrained → least-loss model saved and hot-swapped into memory immediately.

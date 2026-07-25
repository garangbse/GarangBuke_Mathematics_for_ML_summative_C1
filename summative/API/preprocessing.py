"""
preprocessing.py

SINGLE SOURCE OF TRUTH for data cleaning + feature engineering.

This file is imported by BOTH:
  1. The Colab notebook (linear_regression/multivariate.ipynb) — for training
  2. The API (API/prediction.py, API/training.py) — for serving predictions
     and for retraining

Keeping this logic in ONE file that both sides import (instead of copy-pasted
notebook cells re-typed by hand into the API) means the cleaning/encoding the
model was TRAINED on and the cleaning/encoding used at PREDICTION time can
never silently drift apart.

How the Colab notebook imports this exact file (no re-typing):
    !curl -O https://raw.githubusercontent.com/garangbse/Garang_Buke_Mathematics_for_Machine_Learning_Summative_Cohort1/summative/API/preprocessing.py
    from preprocessing import clean_raw_dataframe, build_feature_matrix
"""

import numpy as np
import pandas as pd

COLS_TO_SCALE = ["age", "years_of_experience", "rating", "client_satisfaction_clean"]

_ACTIVE_MAP = {"1": 1, "0": 0, "y": 1, "n": 0, "yes": 1, "no": 0, "true": 1, "false": 0}


def _clean_rate(x):
    if pd.isna(x):
        return np.nan
    s = str(x).replace("USD", "").replace("$", "").strip()
    try:
        return float(s)
    except ValueError:
        return np.nan


def _clean_gender(x):
    x = str(x).strip().lower()
    if x in ("m", "male"):
        return "male"
    if x in ("f", "female"):
        return "female"
    return np.nan


def _clean_active(x):
    if pd.isna(x):
        return np.nan
    return _ACTIVE_MAP.get(str(x).strip().lower(), np.nan)


def _clean_pct(x):
    if pd.isna(x):
        return np.nan
    s = str(x).replace("%", "").strip()
    try:
        return float(s)
    except ValueError:
        return np.nan


def clean_raw_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Raw freelancer CSV (messy formats, NaNs) -> fully cleaned DataFrame:
    target parsed, categorical text normalized, all NaNs handled."""
    df = df_raw.copy()

    df["hourly_rate_usd"] = df["hourly_rate (USD)"].apply(_clean_rate)
    df = df.dropna(subset=["hourly_rate_usd"]).reset_index(drop=True)

    df["gender_clean"] = df["gender"].apply(_clean_gender)
    df["is_active_clean"] = df["is_active"].apply(_clean_active)
    df["client_satisfaction_clean"] = df["client_satisfaction"].apply(_clean_pct)

    for col in ["age", "years_of_experience", "rating", "client_satisfaction_clean"]:
        df[col] = df[col].fillna(df[col].median())

    df["gender_clean"] = df["gender_clean"].fillna(df["gender_clean"].mode()[0])
    df["is_active_clean"] = df["is_active_clean"].fillna(df["is_active_clean"].mode()[0])

    return df


def build_feature_matrix(df_clean: pd.DataFrame, reference_columns=None) -> pd.DataFrame:
    """Drops non-predictive/redundant columns, encodes categoricals to numeric.
    If reference_columns is given, the result is reindexed to match those
    exact columns (missing dummy columns filled with 0) -- keeps training and
    single-row prediction schema-compatible."""
    drop_cols = ["freelancer_ID", "name", "language", "gender", "is_active",
                 "client_satisfaction", "hourly_rate (USD)"]
    df_model = df_clean.drop(columns=[c for c in drop_cols if c in df_clean.columns])

    df_model["gender_num"] = (df_model["gender_clean"] == "male").astype(int)
    df_model = df_model.drop(columns=["gender_clean"])

    df_model = pd.get_dummies(df_model, columns=["country", "primary_skill"], drop_first=True)

    if reference_columns is not None:
        target = df_model["hourly_rate_usd"] if "hourly_rate_usd" in df_model.columns else None
        df_model = df_model.reindex(columns=reference_columns, fill_value=0)
        if target is not None:
            df_model["hourly_rate_usd"] = target.values

    return df_model


def build_single_record_row(record: dict, feature_cols: list, medians: dict) -> dict:
    """Turns one incoming API request (a dict of raw field values) into a
    feature row dict aligned to feature_cols -- same encoding rules as
    build_feature_matrix, just for a single record instead of a DataFrame."""
    row = {col: 0 for col in feature_cols}

    row["age"] = record.get("age", medians["age"])
    row["years_of_experience"] = record.get("years_of_experience", medians["years_of_experience"])
    row["rating"] = record.get("rating", medians["rating"])

    gender_str = str(record.get("gender", "male")).strip().lower()
    row["gender_num"] = 1 if gender_str in ("m", "male") else 0

    row["is_active_clean"] = _ACTIVE_MAP.get(str(record.get("is_active", 1)).strip().lower(), 1)

    sat_raw = record.get("client_satisfaction", None)
    row["client_satisfaction_clean"] = (
        medians["client_satisfaction_clean"] if sat_raw is None
        else float(str(sat_raw).replace("%", "").strip())
    )

    country_col = f"country_{record['country']}"
    if country_col in row:
        row[country_col] = 1

    skill_col = f"primary_skill_{record['primary_skill']}"
    if skill_col in row:
        row[skill_col] = 1

    return row

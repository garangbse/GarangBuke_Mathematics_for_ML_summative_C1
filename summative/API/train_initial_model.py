"""
train_initial_model.py

Run this ONCE to train the initial model and populate artifacts/.
Uses training.py, which itself uses preprocessing.py -- no logic duplicated.

Usage:
    uv run python train_initial_model.py
"""
import os
import shutil
import pandas as pd

from training import train_and_select_best

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TRAINING_DATA_PATH = os.path.join(DATA_DIR, "training_data.csv")
RAW_DATA_SOURCE = os.path.join(os.path.dirname(__file__), "global_freelancers_raw.csv")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(TRAINING_DATA_PATH):
        shutil.copy(RAW_DATA_SOURCE, TRAINING_DATA_PATH)
        print(f"Copied base dataset to {TRAINING_DATA_PATH}")

    df_raw = pd.read_csv(TRAINING_DATA_PATH)
    summary = train_and_select_best(df_raw)

    print("Training complete. Best model:", summary["best_model"])
    print("Training rows used:", summary["n_training_rows"])
    for m in summary["all_model_metrics"]:
        print(f"  {m['model']:<35} RMSE={m['rmse']:.2f}  R2={m['r2']:.3f}")


if __name__ == "__main__":
    main()

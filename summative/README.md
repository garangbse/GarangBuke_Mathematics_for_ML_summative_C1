# Freelancer Hourly Rate Predictor — Summative Project

## Mission & Problem
Freelance platforms hold rich profile data, yet freelancers rarely get a clear, data-driven signal
for what they should charge per hour. This project builds a regression model that predicts a
freelancer's **hourly rate (USD)** from their profile — gender, age, country, primary skill,
experience, rating, activity status, and client satisfaction — and serves it through an API and a
mobile app so the prediction is usable outside a notebook.

## Live API (public, not localhost)
- **Base URL:** `https://<your-render-app>.onrender.com` — replace after deploying (see `summative/API/README.md`)
- **Swagger UI (test it here):** `https://<your-render-app>.onrender.com/docs`
- **Predict endpoint:** `POST https://<your-render-app>.onrender.com/predict`

## Video Demo
📺 **YouTube (≤7 min):** `<paste your YouTube link here after recording>`

## Repository structure
```
linear_regression_model/
└── summative/
    ├── linear_regression/
    │   └── multivariate.ipynb      # Task 1: data, viz, feature engineering, 4 models, best-model save
    ├── API/
    │   ├── prediction.py           # FastAPI app (Task 2): /predict, /retrain, CORS, Swagger docs
    │   ├── preprocessing.py        # Shared cleaning/encoding logic (also usable from the notebook)
    │   ├── training.py             # Training pipeline used by /retrain
    │   ├── schemas.py              # Pydantic request/response models (types + range constraints)
    │   ├── train_initial_model.py  # One-time script to populate artifacts/
    │   ├── artifacts/              # Saved model + scaler + schema
    │   ├── data/                   # Accumulated training data
    │   ├── global_freelancers_raw.csv
    │   ├── requirements.txt
    │   └── README.md               # Full API run + Render deployment instructions
    ├── FlutterApp/                 # Task 3: single-page Flutter prediction client
    │   ├── lib/main.dart
    │   ├── pubspec.yaml
    │   └── README.md
    ├── pyproject.toml              # uv dependency manifest (whole project)
    └── uv.lock
```

## Running the mobile app
1. Install Flutter: https://docs.flutter.dev/get-started/install
2. `cd linear_regression_model/summative/FlutterApp`
3. Run `flutter create .` once, to generate the platform folders (`android/`, `ios/`, etc.) around the
   provided `lib/main.dart` and `pubspec.yaml`.
4. Open `lib/main.dart` and set `apiBaseUrl` to the live Render URL above (not `localhost`).
5. `flutter pub get`
6. `flutter run` (pick a connected device/emulator, or `flutter run -d chrome` to try it in a browser).

Full details for each piece (API setup with `uv`, Render deployment steps, Flutter run steps) are in
`summative/API/README.md` and `summative/FlutterApp/README.md`.

## Package management
This project uses **uv** for all Python dependency/virtual-environment management —
see `summative/pyproject.toml` and `summative/uv.lock`. From `summative/`:
```bash
uv sync
cd API
uv run --project .. python train_initial_model.py
uv run --project .. uvicorn prediction:app --reload
```

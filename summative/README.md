# Freelancer Hourly Rate Predictor — Summative Project

## Mission & Problem
My mission lies in job creation and a target audience I noticed for this is freelance platforms that hold rich profile data, yet freelancers rarely get a clear, data-driven signal for what they should charge per hour. This project builds a regression model that predicts a freelancer's **hourly rate (USD)** from their profile — gender, age, country, primary skill,experience, rating, activity status, and client satisfaction — and serves it through an API and amobile app so the prediction is usable outside a notebook.

## Live API (public, not localhost)
- **Base URL:** `https://garangbuke-mathematics-for-ml-summative.onrender.com`
- **Swagger UI (test it here):** `https://garangbuke-mathematics-for-ml-summative.onrender.com/docs`
- **Predict endpoint:** `POST https://garangbuke-mathematics-for-ml-summative.onrender.com/predict`

> Before submitting, confirm the deployment is actually live:
> `curl https://garangbuke-mathematics-for-ml-summative.onrender.com/health` should return
> `{"status":"ok","model_loaded":true,...}`. Render's free tier sleeps after inactivity, so the
> first request may take 30-50s to respond — that's normal.

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
    ├── FlutterApp/
    │   └── freelancer_rate_predictor/   # Task 3: Flutter client for freelancer rate prediction
    │       ├── lib/
    │       │   ├── constants/           # API base URL / endpoint / timeout (api_config.dart)
    │       │   ├── models/              # Data models for API requests/responses
    │       │   ├── screens/             # The single prediction page
    │       │   ├── services/            # API communication (prediction_service.dart)
    │       │   ├── widgets/             # Reusable UI components (text field, result display)
    │       │   └── main.dart            # App entry point
    │       ├── pubspec.yaml
    │       └── README.md
    ├── pyproject.toml              # uv dependency manifest (whole project)
    └── uv.lock
```

## Running the mobile app
1. Install Flutter: https://docs.flutter.dev/get-started/install
2. `cd linear_regression_model/summative/FlutterApp/freelancer_rate_predictor`
3. Run `flutter create .` once, to generate the platform folders (`android/`, `ios/`, etc.) around the
   provided `lib/` and `pubspec.yaml`.
   "baseUrl" - https://garangbuke-mathematics-for-ml-summative.onrender.com
4. Open `lib/constants/api_config.dart` and set `baseUrl` to the live Render URL above (not `localhost`).
5. `flutter pub get`
6. `flutter run` (pick a connected device/emulator, or `flutter run -d chrome` to try it in a browser).

Full details for each piece (API setup with `uv`, Render deployment steps, Flutter run steps) are in
`summative/API/README.md` and `summative/FlutterApp/freelancer_rate_predictor/README.md`.

## Package management & virtual environment (uv)
This project uses **uv** for all Python dependency AND virtual-environment management —
see `summative/pyproject.toml` (dependency manifest) and `summative/uv.lock` (locked exact versions).

**From `summative/`:**
```bash
# 1. Create the virtual environment (creates .venv/ from pyproject.toml)
cd API
uv venv

# 2. Activate it (optional -- uv run below works without activating too)
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate         # Windows

# 3. Install all locked dependencies into that environment
uv sync

# 4. Run project commands inside the environment, without needing to activate it first
uv run --project .. python train_initial_model.py
uv run --project .. uvicorn prediction:app --reload
```

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import pandas as pd
import joblib

app = FastAPI(title="ChurnGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Paths ----------
BASE_DIR = Path(__file__).resolve().parents[2]   # project root
MODEL_PATH = BASE_DIR / "src" / "models" / "churn_model.pkl"
COLUMNS_PATH = BASE_DIR / "src" / "models" / "model_columns.pkl"
DATA_PATH = BASE_DIR / "data" / "raw" / "IBM Teleco Churn Dataset.csv"
PREDICTIONS_DIR = BASE_DIR / "data" / "processed"
PREDICTIONS_PATH = PREDICTIONS_DIR / "prediction_history.csv"

PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)

# ---------- Load artifacts ----------
model = joblib.load(MODEL_PATH)
model_columns = joblib.load(COLUMNS_PATH)

# ---------- Request schema ----------
class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


# ---------- Helpers ----------
def risk_category(p: float) -> str:
    if p < 0.3:
        return "Low Risk"
    elif p < 0.7:
        return "Medium Risk"
    else:
        return "High Risk"


def retention_action(row: dict) -> str:
    actions = []

    if row["Contract"] == "Month-to-month":
        actions.append("Offer long-term contract discount")

    if row["MonthlyCharges"] > 70:
        actions.append("Provide discount or bundle offer")

    if row["tenure"] < 12:
        actions.append("Onboarding support / engagement program")

    if row["TechSupport"] == "No":
        actions.append("Offer free tech support trial")

    if not actions:
        return "No immediate action"

    return ", ".join(actions)


def ensure_dataset_loaded() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())
    return df


def append_prediction_record(input_dict: dict, churn_prob: float, churn_pred: int, risk: str, action: str):
    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        **input_dict,
        "churn_probability": round(float(churn_prob), 4),
        "churn_prediction": int(churn_pred),
        "risk_level": risk,
        "retention_action": action,
    }

    row_df = pd.DataFrame([row])

    if PREDICTIONS_PATH.exists():
        row_df.to_csv(PREDICTIONS_PATH, mode="a", header=False, index=False)
    else:
        row_df.to_csv(PREDICTIONS_PATH, index=False)


def load_prediction_history() -> pd.DataFrame:
    if PREDICTIONS_PATH.exists():
        return pd.read_csv(PREDICTIONS_PATH)
    return pd.DataFrame()


# ---------- Routes ----------
@app.get("/")
def home():
    return {"message": "ChurnGuard API is running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": MODEL_PATH.exists(),
        "columns_loaded": COLUMNS_PATH.exists(),
        "dataset_loaded": DATA_PATH.exists(),
        "prediction_history_exists": PREDICTIONS_PATH.exists(),
    }


@app.post("/predict")
def predict(data: CustomerData):
    input_dict = data.model_dump()
    input_df = pd.DataFrame([input_dict])

    # keep original values for retention logic + history
    original_row = input_df.iloc[0].to_dict()

    # one-hot encode input
    input_encoded = pd.get_dummies(input_df)

    # align with training columns
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

    # predict
    churn_prob = model.predict_proba(input_encoded)[0][1]
    churn_pred = int(churn_prob >= 0.5)
    risk = risk_category(churn_prob)
    action = retention_action(original_row)

    append_prediction_record(original_row, churn_prob, churn_pred, risk, action)

    return {
        "churn_probability": round(float(churn_prob), 4),
        "churn_prediction": churn_pred,
        "risk_level": risk,
        "retention_action": action,
    }


@app.get("/metrics")
def metrics():
    df = ensure_dataset_loaded()
    history = load_prediction_history()

    total_customers = int(len(df))
    churn_rate = round(float((df["Churn"] == "Yes").mean() * 100), 2)

    high_risk_customers = 0
    if not history.empty:
        high_risk_customers = int((history["risk_level"] == "High Risk").sum())

    revenue_at_risk = 0.0
    if not history.empty and "MonthlyCharges" in history.columns:
        high_risk_df = history[history["risk_level"] == "High Risk"]
        revenue_at_risk = round(float(high_risk_df["MonthlyCharges"].sum()), 2)

    return {
        "total_customers": total_customers,
        "churn_rate": churn_rate,
        "high_risk_customers": high_risk_customers,
        "predicted_revenue_at_risk": revenue_at_risk,
        "total_predictions_made": int(len(history)),
    }


@app.get("/risk-distribution")
def risk_distribution():
    history = load_prediction_history()

    if history.empty:
        return {
            "labels": ["Low Risk", "Medium Risk", "High Risk"],
            "values": [0, 0, 0],
        }

    order = ["Low Risk", "Medium Risk", "High Risk"]
    counts = history["risk_level"].value_counts()
    values = [int(counts.get(label, 0)) for label in order]

    return {
        "labels": order,
        "values": values,
    }


@app.get("/contract-churn")
def contract_churn():
    df = ensure_dataset_loaded()

    summary = (
        df.groupby("Contract")["Churn"]
        .apply(lambda x: round((x == "Yes").mean() * 100, 2))
        .reset_index(name="churn_rate")
        .sort_values("churn_rate", ascending=False)
    )

    return summary.to_dict(orient="records")


@app.get("/payment-method-churn")
def payment_method_churn():
    df = ensure_dataset_loaded()

    summary = (
        df.groupby("PaymentMethod")["Churn"]
        .apply(lambda x: round((x == "Yes").mean() * 100, 2))
        .reset_index(name="churn_rate")
        .sort_values("churn_rate", ascending=False)
    )

    return summary.to_dict(orient="records")


@app.get("/recent-predictions")
def recent_predictions(limit: int = 10):
    history = load_prediction_history()

    if history.empty:
        return []

    history = history.sort_values("timestamp", ascending=False).head(limit)

    cols = [
        "timestamp",
        "Contract",
        "MonthlyCharges",
        "churn_probability",
        "churn_prediction",
        "risk_level",
        "retention_action",
    ]

    existing_cols = [c for c in cols if c in history.columns]
    return history[existing_cols].to_dict(orient="records")
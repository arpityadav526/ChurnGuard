from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
from io import StringIO
import pandas as pd
import joblib

app = FastAPI(title="ChurnGuard API", version="1.0.0")

# Streamlit-friendly CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "src" / "models" / "churn_model.pkl"
COLUMNS_PATH = BASE_DIR / "src" / "models" / "model_columns.pkl"
METRICS_PATH = BASE_DIR / "src" / "models" / "model_metrics.pkl"
DATA_PATH = BASE_DIR / "data" / "raw" / "IBM Teleco Churn Dataset.csv"

PREDICTIONS_DIR = BASE_DIR / "data" / "processed"
PREDICTIONS_PATH = PREDICTIONS_DIR / "prediction_history.csv"

PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)

if not MODEL_PATH.exists():
    raise RuntimeError(f"Model file not found at: {MODEL_PATH}")

if not COLUMNS_PATH.exists():
    raise RuntimeError(f"Model columns file not found at: {COLUMNS_PATH}")

model = joblib.load(MODEL_PATH)
model_columns = joblib.load(COLUMNS_PATH)

if METRICS_PATH.exists():
    model_metrics = joblib.load(METRICS_PATH)
else:
    model_metrics = None

print("Loaded model type:", type(model))
print("Loaded model from:", MODEL_PATH)
print("Loaded columns from:", COLUMNS_PATH)

if model_metrics is not None:
    print("Loaded metrics from:", METRICS_PATH)
else:
    print("Model metrics file not found.")

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


REQUIRED_COLUMNS = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
]


def risk_category(p: float) -> str:
    if p < 0.3:
        return "Low Risk"
    elif p < 0.7:
        return "Medium Risk"
    return "High Risk"


def retention_action(row: dict) -> str:
    actions = []

    if row.get("Contract") == "Month-to-month":
        actions.append("Offer long-term contract discount")

    if float(row.get("MonthlyCharges", 0)) > 70:
        actions.append("Provide discount or bundle offer")

    if float(row.get("tenure", 0)) < 12:
        actions.append("Onboarding support / engagement program")

    if row.get("TechSupport") == "No":
        actions.append("Offer free tech support trial")

    if row.get("OnlineSecurity") == "No":
        actions.append("Bundle online security service")

    if row.get("PaymentMethod") == "Electronic check":
        actions.append("Encourage shift to automatic payment methods")

    if not actions:
        return "No immediate action"

    return ", ".join(actions[:2])


def ensure_dataset_loaded() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Raw dataset not found.")

    df = pd.read_csv(DATA_PATH)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())
    return df


def append_prediction_record(
    input_dict: dict,
    churn_prob: float,
    churn_pred: int,
    risk: str,
    action: str
):
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


def preprocess_input_df(input_df: pd.DataFrame) -> pd.DataFrame:
    processed_df = input_df.copy()

    if "TotalCharges" in processed_df.columns:
        processed_df["TotalCharges"] = pd.to_numeric(
            processed_df["TotalCharges"], errors="coerce"
        )
        processed_df["TotalCharges"] = processed_df["TotalCharges"].fillna(
            processed_df["TotalCharges"].median()
        )

    # Must match training exactly
    processed_df["AvgCharges"] = processed_df["TotalCharges"] / (processed_df["tenure"] + 1)
    processed_df["IsNewCustomer"] = (processed_df["tenure"] <= 12).astype(int)
    processed_df["HighSpender"] = (processed_df["MonthlyCharges"] >= 80).astype(int)

    encoded_df = pd.get_dummies(processed_df)
    encoded_df = encoded_df.reindex(columns=model_columns, fill_value=0)

    return encoded_df


def validate_input_columns(df: pd.DataFrame):
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {missing_cols}"
        )


def build_customer_drivers(row: dict) -> list[dict]:
    drivers = []

    if row.get("Contract") == "Month-to-month":
        drivers.append({
            "title": "Month-to-Month Contract",
            "description": "Customers on month-to-month plans usually show higher churn probability than long-term contract users.",
            "impact": "High"
        })

    if float(row.get("MonthlyCharges", 0)) >= 80:
        drivers.append({
            "title": "High Monthly Charges",
            "description": "Higher monthly bills are strongly associated with elevated churn risk.",
            "impact": "High"
        })

    if float(row.get("tenure", 0)) <= 12:
        drivers.append({
            "title": "Low Tenure",
            "description": "Newer customers are more likely to leave early if engagement is weak.",
            "impact": "High"
        })

    if row.get("TechSupport") == "No":
        drivers.append({
            "title": "No Tech Support",
            "description": "Lack of tech support often increases dissatisfaction and churn likelihood.",
            "impact": "Medium"
        })

    if row.get("OnlineSecurity") == "No":
        drivers.append({
            "title": "No Online Security",
            "description": "Customers without online security services tend to show weaker service stickiness.",
            "impact": "Medium"
        })

    if row.get("PaymentMethod") == "Electronic check":
        drivers.append({
            "title": "Electronic Check Payment",
            "description": "Electronic check users tend to churn more often than customers on other payment methods.",
            "impact": "Medium"
        })

    if row.get("InternetService") == "Fiber optic":
        drivers.append({
            "title": "Fiber Optic Service",
            "description": "In this dataset, fiber optic customers often show relatively higher churn.",
            "impact": "Medium"
        })

    if row.get("Partner") == "No":
        drivers.append({
            "title": "No Partner",
            "description": "Customers without a partner may have slightly weaker retention in some churn patterns.",
            "impact": "Low"
        })

    if not drivers:
        drivers.append({
            "title": "Stable Customer Profile",
            "description": "This customer does not currently show strong churn signals from the available rules.",
            "impact": "Low"
        })

    return drivers[:5]


def build_explanation_bars(row: dict) -> list[dict]:
    bars = []

    if row.get("Contract") == "Month-to-month":
        bars.append({
            "feature": "Month-to-Month Contract",
            "value": 0.30,
            "direction": "increase"
        })

    if float(row.get("MonthlyCharges", 0)) >= 80:
        bars.append({
            "feature": "High Monthly Charges",
            "value": 0.22,
            "direction": "increase"
        })

    if float(row.get("tenure", 0)) <= 12:
        bars.append({
            "feature": "Low Tenure",
            "value": 0.20,
            "direction": "increase"
        })

    if row.get("TechSupport") == "No":
        bars.append({
            "feature": "No Tech Support",
            "value": 0.12,
            "direction": "increase"
        })

    if row.get("OnlineSecurity") == "No":
        bars.append({
            "feature": "No Online Security",
            "value": 0.10,
            "direction": "increase"
        })

    if row.get("PaymentMethod") == "Electronic check":
        bars.append({
            "feature": "Electronic Check",
            "value": 0.08,
            "direction": "increase"
        })

    if row.get("Partner") == "Yes":
        bars.append({
            "feature": "Has Partner",
            "value": 0.06,
            "direction": "decrease"
        })

    if float(row.get("tenure", 0)) >= 36:
        bars.append({
            "feature": "Long Tenure",
            "value": 0.12,
            "direction": "decrease"
        })

    if row.get("Contract") in ["One year", "Two year"]:
        bars.append({
            "feature": "Long-Term Contract",
            "value": 0.14,
            "direction": "decrease"
        })

    if not bars:
        bars.append({
            "feature": "Balanced Profile",
            "value": 0.01,
            "direction": "decrease"
        })

    return bars[:6]


def get_global_feature_importance() -> list[dict]:
    return [
        {"feature": "Contract Type", "score": 92},
        {"feature": "Monthly Charges", "score": 84},
        {"feature": "Tenure", "score": 79},
        {"feature": "Tech Support", "score": 63},
        {"feature": "Online Security", "score": 58},
        {"feature": "Payment Method", "score": 52},
        {"feature": "Internet Service", "score": 47},
    ]


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

    original_row = input_df.iloc[0].to_dict()
    input_encoded = preprocess_input_df(input_df)

    churn_prob = float(model.predict_proba(input_encoded)[0][1])
    churn_pred = int(churn_prob >= 0.5)
    risk = risk_category(churn_prob)
    action = retention_action(original_row)
    drivers = build_customer_drivers(original_row)
    explanation_bars = build_explanation_bars(original_row)

    append_prediction_record(original_row, churn_prob, churn_pred, risk, action)

    return {
        "churn_probability": round(churn_prob, 4),
        "churn_prediction": churn_pred,
        "risk_level": risk,
        "retention_action": action,
        "top_drivers": drivers,
        "explanation_bars": explanation_bars,
    }


@app.post("/predict-batch")
async def predict_batch(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = await file.read()

    try:
        df = pd.read_csv(StringIO(content.decode("utf-8")))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file.")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded CSV is empty.")

    validate_input_columns(df)

    original_df = df.copy()
    processed_df = preprocess_input_df(df)

    probs = model.predict_proba(processed_df)[:, 1]
    preds = (probs >= 0.5).astype(int)

    original_df["churn_probability"] = probs.round(4)
    original_df["churn_prediction"] = preds
    original_df["risk_level"] = [risk_category(p) for p in probs]
    original_df["retention_action"] = [
        retention_action(row) for row in original_df.to_dict(orient="records")
    ]
    original_df["top_drivers"] = [
        build_customer_drivers(row) for row in original_df.to_dict(orient="records")
    ]

    for row in original_df.to_dict(orient="records"):
        append_prediction_record(
            input_dict={k: row[k] for k in REQUIRED_COLUMNS},
            churn_prob=row["churn_probability"],
            churn_pred=row["churn_prediction"],
            risk=row["risk_level"],
            action=row["retention_action"],
        )

    high_risk_count = int((original_df["risk_level"] == "High Risk").sum())

    return {
        "total_rows": int(len(original_df)),
        "high_risk_count": high_risk_count,
        "predictions": original_df.to_dict(orient="records"),
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


@app.get("/insights/latest-customer")
def insights_latest_customer():
    history = load_prediction_history()

    if history.empty:
        return {"message": "No prediction history found yet."}

    history = history.sort_values("timestamp", ascending=False)
    row = history.iloc[0].to_dict()

    return {
        "customer_profile": {
            "timestamp": row.get("timestamp"),
            "contract": row.get("Contract"),
            "monthly_charges": round(float(row.get("MonthlyCharges", 0)), 2),
            "tenure": int(row.get("tenure", 0)),
            "internet_service": row.get("InternetService"),
            "payment_method": row.get("PaymentMethod"),
        },
        "churn_probability": round(float(row.get("churn_probability", 0)), 4),
        "churn_prediction": int(row.get("churn_prediction", 0)),
        "risk_level": row.get("risk_level", "Unknown"),
        "retention_action": row.get("retention_action", "No action"),
        "top_drivers": build_customer_drivers(row),
        "explanation_bars": build_explanation_bars(row),
    }


@app.get("/insights/customer")
def insights_customer(index: int = 0):
    history = load_prediction_history()

    if history.empty:
        return {"message": "No prediction history found yet."}

    history = history.sort_values("timestamp", ascending=False).reset_index(drop=True)

    if index < 0 or index >= len(history):
        return {"message": "Customer index out of range."}

    row = history.iloc[index].to_dict()

    return {
        "customer_profile": {
            "timestamp": row.get("timestamp"),
            "contract": row.get("Contract"),
            "monthly_charges": round(float(row.get("MonthlyCharges", 0)), 2),
            "tenure": int(row.get("tenure", 0)),
            "internet_service": row.get("InternetService"),
            "payment_method": row.get("PaymentMethod"),
        },
        "churn_probability": round(float(row.get("churn_probability", 0)), 4),
        "churn_prediction": int(row.get("churn_prediction", 0)),
        "risk_level": row.get("risk_level", "Unknown"),
        "retention_action": row.get("retention_action", "No action"),
        "top_drivers": build_customer_drivers(row),
        "explanation_bars": build_explanation_bars(row),
    }


@app.get("/insights/feature-importance")
def insights_feature_importance():
    return get_global_feature_importance()


@app.get("/model-performance")
def model_performance():
    return model_metrics

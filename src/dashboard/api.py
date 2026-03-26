from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
from io import StringIO
import pandas as pd
import joblib
import sqlite3
import shap
import numpy as np
import os
from dotenv import load_dotenv

# IMPORTANT:
# Change this import path if your feature_engineering.py is stored elsewhere.
from src.models.feature_engineering import add_features

load_dotenv()

app = FastAPI(title="ChurnGuard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "https://churnguard526.streamlit.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = Path(os.getenv("MODEL_PATH", str(BASE_DIR / "src" / "models" / "churn_model.pkl")))
COLUMNS_PATH = Path(os.getenv("COLUMNS_PATH", str(BASE_DIR / "src" / "models" / "model_columns.pkl")))
METRICS_PATH = Path(os.getenv("METRICS_PATH", str(BASE_DIR / "src" / "models" / "model_metrics.pkl")))
DATA_PATH = Path(os.getenv("DATA_PATH", str(BASE_DIR / "data" / "raw" / "IBM Teleco Churn Dataset.csv")))

PREDICTIONS_DIR = Path(os.getenv("PREDICTIONS_DIR", str(BASE_DIR / "data" / "processed")))
DB_PATH = Path(os.getenv("DB_PATH", str(PREDICTIONS_DIR / "churnguard.db")))
PREDICTIONS_PATH = Path(os.getenv("PREDICTIONS_PATH", str(PREDICTIONS_DIR / "prediction_history.csv")))

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

try:
    explainer = shap.TreeExplainer(model)
    print("SHAP TreeExplainer initialized successfully.")
except Exception as e:
    explainer = None
    print("Failed to initialize SHAP TreeExplainer:", str(e))


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

ENGINEERED_COLUMNS = [
    "AvgMonthlySpend",
    "TenureGroup",
    "TotalServices",
    "ContractRisk",
]


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            gender TEXT,
            SeniorCitizen INTEGER,
            Partner TEXT,
            Dependents TEXT,
            tenure INTEGER,
            PhoneService TEXT,
            MultipleLines TEXT,
            InternetService TEXT,
            OnlineSecurity TEXT,
            OnlineBackup TEXT,
            DeviceProtection TEXT,
            TechSupport TEXT,
            StreamingTV TEXT,
            StreamingMovies TEXT,
            Contract TEXT,
            PaperlessBilling TEXT,
            PaymentMethod TEXT,
            MonthlyCharges REAL,
            TotalCharges REAL,
            churn_probability REAL,
            churn_prediction INTEGER,
            risk_level TEXT,
            retention_action TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


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
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            timestamp, gender, SeniorCitizen, Partner, Dependents, tenure,
            PhoneService, MultipleLines, InternetService, OnlineSecurity,
            OnlineBackup, DeviceProtection, TechSupport, StreamingTV,
            StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
            MonthlyCharges, TotalCharges, churn_probability, churn_prediction,
            risk_level, retention_action
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(timespec="seconds"),
        input_dict.get("gender"),
        input_dict.get("SeniorCitizen"),
        input_dict.get("Partner"),
        input_dict.get("Dependents"),
        input_dict.get("tenure"),
        input_dict.get("PhoneService"),
        input_dict.get("MultipleLines"),
        input_dict.get("InternetService"),
        input_dict.get("OnlineSecurity"),
        input_dict.get("OnlineBackup"),
        input_dict.get("DeviceProtection"),
        input_dict.get("TechSupport"),
        input_dict.get("StreamingTV"),
        input_dict.get("StreamingMovies"),
        input_dict.get("Contract"),
        input_dict.get("PaperlessBilling"),
        input_dict.get("PaymentMethod"),
        float(input_dict.get("MonthlyCharges", 0)),
        float(input_dict.get("TotalCharges", 0)),
        round(float(churn_prob), 4),
        int(churn_pred),
        risk,
        action
    ))

    conn.commit()
    conn.close()


def load_prediction_history() -> pd.DataFrame:
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM predictions", conn)
    conn.close()
    return df


def preprocess_input_df(input_df: pd.DataFrame) -> pd.DataFrame:
    processed_df = input_df.copy()

    if "TotalCharges" in processed_df.columns:
        processed_df["TotalCharges"] = pd.to_numeric(
            processed_df["TotalCharges"], errors="coerce"
        )
        processed_df["TotalCharges"] = processed_df["TotalCharges"].fillna(
            processed_df["TotalCharges"].median()
        )

    # Apply SAME feature engineering as training
    processed_df = add_features(processed_df)

    # If add_features accidentally receives Churn in some cases, remove it
    if "Churn" in processed_df.columns:
        processed_df = processed_df.drop(columns=["Churn"])

    # Match training encoding logic
    cat_cols = processed_df.select_dtypes(include=["object"]).columns
    encoded_df = pd.get_dummies(processed_df, columns=cat_cols, drop_first=True)

    # Align with training columns
    encoded_df = encoded_df.reindex(columns=model_columns, fill_value=0)

    return encoded_df


def validate_input_columns(df: pd.DataFrame):
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {missing_cols}"
        )


def prettify_feature_name(name: str) -> str:
    pretty_map = {
        "SeniorCitizen": "Senior Citizen",
        "PhoneService": "Phone Service",
        "MultipleLines": "Multiple Lines",
        "InternetService": "Internet Service",
        "OnlineSecurity": "Online Security",
        "OnlineBackup": "Online Backup",
        "DeviceProtection": "Device Protection",
        "TechSupport": "Tech Support",
        "StreamingTV": "Streaming TV",
        "StreamingMovies": "Streaming Movies",
        "PaperlessBilling": "Paperless Billing",
        "PaymentMethod": "Payment Method",
        "MonthlyCharges": "Monthly Charges",
        "TotalCharges": "Total Charges",
        "AvgMonthlySpend": "Average Monthly Spend",
        "TenureGroup": "Tenure Group",
        "TotalServices": "Total Services",
        "ContractRisk": "Contract Risk",
    }
    return pretty_map.get(name, name)


def get_feature_group(feature_name: str) -> str:
    all_groups = REQUIRED_COLUMNS + ENGINEERED_COLUMNS

    for col in all_groups:
        if feature_name == col:
            return col
        if feature_name.startswith(f"{col}_"):
            return col

    # handle one-hot tenure group names explicitly
    if feature_name.startswith("TenureGroup_"):
        return "TenureGroup"

    return feature_name


def get_display_value(feature_group: str, original_row: dict) -> str:
    if feature_group in original_row:
        return str(original_row.get(feature_group))

    if feature_group == "AvgMonthlySpend":
        tenure = float(original_row.get("tenure", 0))
        total = float(original_row.get("TotalCharges", 0))
        return str(round(total / (tenure + 1), 2))

    if feature_group == "TenureGroup":
        tenure = float(original_row.get("tenure", 0))
        if tenure <= 12:
            return "New"
        elif tenure <= 24:
            return "Mid"
        else:
            return "Loyal"

    if feature_group == "TotalServices":
        service_mapping = {
            "No": 0,
            "Yes": 1,
            "No internet service": 0,
            "No phone service": 0,
            "Fiber optic": 1,
            "DSL": 1,
        }

        service_cols = [
            "PhoneService", "MultipleLines", "InternetService",
            "OnlineSecurity", "OnlineBackup", "DeviceProtection",
            "TechSupport", "StreamingTV", "StreamingMovies"
        ]

        total = 0
        for col in service_cols:
            total += service_mapping.get(original_row.get(col), 0)

        return str(total)

    if feature_group == "ContractRisk":
        contract = original_row.get("Contract")
        contract_map = {
            "Month-to-month": 2,
            "One year": 1,
            "Two year": 0
        }
        return str(contract_map.get(contract, "N/A"))

    return "N/A"


def impact_level(abs_value: float) -> str:
    if abs_value >= 0.08:
        return "High"
    if abs_value >= 0.03:
        return "Medium"
    return "Low"


def build_driver_description(feature_group: str, value: str, shap_value: float) -> str:
    direction_text = "increases" if shap_value > 0 else "reduces"

    custom_descriptions = {
        "Contract": f"Contract setting ({value}) {direction_text} churn risk for this prediction.",
        "MonthlyCharges": f"Monthly charges ({value}) {direction_text} churn risk for this customer.",
        "tenure": f"Customer tenure ({value}) {direction_text} churn risk in the model output.",
        "TechSupport": f"Tech support status ({value}) {direction_text} churn risk for this case.",
        "OnlineSecurity": f"Online security status ({value}) {direction_text} churn risk for this case.",
        "PaymentMethod": f"Payment method ({value}) {direction_text} churn risk in this prediction.",
        "InternetService": f"Internet service type ({value}) {direction_text} churn risk for this customer.",
        "Partner": f"Partner status ({value}) {direction_text} churn risk in the current prediction.",
        "TotalCharges": f"Total charges ({value}) {direction_text} churn risk in the model output.",
        "AvgMonthlySpend": f"Average monthly spend ({value}) {direction_text} churn risk after feature engineering.",
        "TenureGroup": f"Tenure group ({value}) {direction_text} churn risk for this customer segment.",
        "TotalServices": f"Total subscribed services ({value}) {direction_text} churn risk in the model.",
        "ContractRisk": f"Contract risk score ({value}) {direction_text} churn risk in the model.",
    }

    return custom_descriptions.get(
        feature_group,
        f"{prettify_feature_name(feature_group)} ({value}) {direction_text} churn risk for this prediction."
    )


def explain_with_shap(input_df: pd.DataFrame) -> dict:
    if explainer is None:
        return {
            "explanation_type": "shap_unavailable",
            "top_drivers": [],
            "explanation_bars": [],
        }

    processed = preprocess_input_df(input_df)
    original_row = input_df.iloc[0].to_dict()

    try:
        shap_values_raw = explainer.shap_values(processed)
        expected_value = explainer.expected_value
    except Exception:
        shap_explanation = explainer(processed)
        shap_values_raw = shap_explanation.values
        expected_value = shap_explanation.base_values

    if isinstance(shap_values_raw, list):
        if len(shap_values_raw) > 1:
            shap_values = np.array(shap_values_raw[1])
            base_value = expected_value[1] if isinstance(expected_value, (list, np.ndarray)) else expected_value
        else:
            shap_values = np.array(shap_values_raw[0])
            base_value = expected_value[0] if isinstance(expected_value, (list, np.ndarray)) else expected_value
    else:
        shap_values = np.array(shap_values_raw)
        if shap_values.ndim == 3:
            shap_values = shap_values[:, :, 1]
            base_value = expected_value[:, 1][0] if isinstance(expected_value, np.ndarray) and np.array(expected_value).ndim == 2 else expected_value[1]
        else:
            if isinstance(expected_value, np.ndarray):
                base_value = expected_value[0] if expected_value.ndim > 0 else float(expected_value)
            else:
                base_value = expected_value

    row_shap = shap_values[0]
    encoded_feature_names = list(processed.columns)

    grouped_contributions = {}
    for feature_name, shap_val in zip(encoded_feature_names, row_shap):
        group = get_feature_group(feature_name)
        grouped_contributions[group] = grouped_contributions.get(group, 0.0) + float(shap_val)

    driver_rows = []
    for feature_group, shap_val in grouped_contributions.items():
        value = get_display_value(feature_group, original_row)
        abs_val = abs(shap_val)
        direction = "increase" if shap_val > 0 else "decrease"

        driver_rows.append({
            "feature_key": feature_group,
            "title": prettify_feature_name(feature_group),
            "description": build_driver_description(feature_group, value, shap_val),
            "impact": impact_level(abs_val),
            "direction": direction,
            "value": value,
            "shap_value": round(float(shap_val), 6),
            "abs_shap_value": round(float(abs_val), 6),
        })

    driver_rows = sorted(driver_rows, key=lambda x: x["abs_shap_value"], reverse=True)

    top_drivers = driver_rows[:5]
    explanation_bars = [
        {
            "feature": row["title"],
            "value": round(float(row["abs_shap_value"]), 6),
            "direction": row["direction"],
            "shap_value": row["shap_value"],
            "raw_value": row["value"],
        }
        for row in top_drivers
    ]

    return {
        "explanation_type": "model_native_shap",
        "base_value": round(float(base_value), 6) if base_value is not None else None,
        "top_drivers": top_drivers,
        "explanation_bars": explanation_bars,
    }


def get_global_feature_importance() -> list[dict]:
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        grouped_scores = {}

        for feature_name, score in zip(model_columns, importances):
            group = get_feature_group(feature_name)
            grouped_scores[group] = grouped_scores.get(group, 0.0) + float(score)

        ranked = sorted(grouped_scores.items(), key=lambda x: x[1], reverse=True)[:10]

        return [
            {
                "feature": prettify_feature_name(name),
                "score": round(score * 100, 2)
            }
            for name, score in ranked
        ]

    return [
        {"feature": "Contract", "score": 92},
        {"feature": "Monthly Charges", "score": 84},
        {"feature": "Tenure", "score": 79},
        {"feature": "Average Monthly Spend", "score": 67},
        {"feature": "Total Services", "score": 58},
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
        "database_exists": DB_PATH.exists(),
        "shap_ready": explainer is not None,
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

    shap_result = explain_with_shap(input_df)

    append_prediction_record(original_row, churn_prob, churn_pred, risk, action)

    return {
        "churn_probability": round(churn_prob, 4),
        "churn_prediction": churn_pred,
        "risk_level": risk,
        "retention_action": action,
        "explanation_type": shap_result.get("explanation_type", "unknown"),
        "base_value": shap_result.get("base_value"),
        "top_drivers": shap_result.get("top_drivers", []),
        "explanation_bars": shap_result.get("explanation_bars", []),
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

    top_drivers_list = []
    explanation_bars_list = []
    for row in original_df.to_dict(orient="records"):
        row_df = pd.DataFrame([{
            k: row[k] for k in REQUIRED_COLUMNS
        }])
        shap_result = explain_with_shap(row_df)
        top_drivers_list.append(shap_result.get("top_drivers", []))
        explanation_bars_list.append(shap_result.get("explanation_bars", []))

    original_df["top_drivers"] = top_drivers_list
    original_df["explanation_bars"] = explanation_bars_list

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

    input_df = pd.DataFrame([{
        col: row.get(col) for col in REQUIRED_COLUMNS
    }])
    shap_result = explain_with_shap(input_df)

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
        "explanation_type": shap_result.get("explanation_type", "unknown"),
        "top_drivers": shap_result.get("top_drivers", []),
        "explanation_bars": shap_result.get("explanation_bars", []),
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

    input_df = pd.DataFrame([{
        col: row.get(col) for col in REQUIRED_COLUMNS
    }])
    shap_result = explain_with_shap(input_df)

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
        "explanation_type": shap_result.get("explanation_type", "unknown"),
        "top_drivers": shap_result.get("top_drivers", []),
        "explanation_bars": shap_result.get("explanation_bars", []),
    }


@app.get("/insights/feature-importance")
def insights_feature_importance():
    return get_global_feature_importance()


@app.get("/model-performance")
def model_performance():
    if model_metrics is None:
        raise HTTPException(status_code=500, detail="Model metrics not found.")
    return model_metrics
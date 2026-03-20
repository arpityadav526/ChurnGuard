from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd 
import joblib
import os


app = FastAPI(title="ChurnGuard API")

# Load model and training columns
model = joblib.load("src/models/churn_model.pkl")
model_columns = joblib.load("src/models/model_columns.pkl")


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


def risk_category(p):
        if p <0.3:
            return "Low Risk"
        elif p<0.7:
            return "Medium Risk"

        else:
            return "High Risk"

def retention_action(row):
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



@app.get('/')
def Home():
    return {"message": "ChurnGuard API is running"}


@app.post('/predict')
def predict(data: CustomerData):
    input_dict = data.dict()
    input_df = pd.DataFrame([input_dict])

    original_row = input_df.iloc[0].to_dict()

    # One-hot encode input
    input_encoded = pd.get_dummies(input_df)

    # Align with training columns
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

    # Predict
    churn_prob = model.predict_proba(input_encoded)[0][1]
    churn_pred = int(churn_prob >= 0.5)
    risk = risk_category(churn_prob)

    action = retention_action(original_row)

    return {
        "churn_probability": round(float(churn_prob), 4),
        "churn_prediction": churn_pred,
        "risk_level": risk,
        "retention_action": action
    }


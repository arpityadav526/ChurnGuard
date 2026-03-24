import streamlit as st
import pandas as pd
from components.helpers import post_json, safe_dataframe

st.title("Predict Customer Churn")

threshold = st.slider(
    "Decision Threshold",
    min_value=0.10,
    max_value=0.90,
    value=0.50,
    step=0.05,
    help="Lower threshold catches more potential churners but may increase false positives."
)

with st.form("predict_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
        Partner = st.selectbox("Partner", ["Yes", "No"])
        Dependents = st.selectbox("Dependents", ["Yes", "No"])
        tenure = st.number_input("Tenure", min_value=0, max_value=100, value=12)
        PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
        MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

    with col2:
        InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        OnlineSecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        OnlineBackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        DeviceProtection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        TechSupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
        StreamingTV = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

    with col3:
        Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
        PaymentMethod = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )
        MonthlyCharges = st.number_input("Monthly Charges", min_value=0.0, value=70.0, step=0.1)
        TotalCharges = st.number_input("Total Charges", min_value=0.0, value=1500.0, step=0.1)

    submitted = st.form_submit_button("Predict Churn")

if submitted:
    if MonthlyCharges < 0 or TotalCharges < 0 or tenure < 0:
        st.error("Numeric values cannot be negative.")
        st.stop()

    if tenure == 0 and TotalCharges > 0:
        st.warning("Tenure is 0 but Total Charges is greater than 0. Please recheck the input.")

    payload = {
        "gender": gender,
        "SeniorCitizen": SeniorCitizen,
        "Partner": Partner,
        "Dependents": Dependents,
        "tenure": tenure,
        "PhoneService": PhoneService,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies,
        "Contract": Contract,
        "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges,
    }

    with st.spinner("Getting prediction..."):
        result = post_json("/predict", payload)

    if result is None:
        st.stop()

    churn_probability = result.get("churn_probability", 0.0)
    model_prediction = result.get("churn_prediction", 0)
    churn_prediction = 1 if churn_probability >= threshold else 0
    risk_level = result.get("risk_level", "Unknown")
    retention_action = result.get("retention_action", "No action")
    top_drivers = result.get("top_drivers", [])
    explanation_bars = result.get("explanation_bars", [])
    explanation_type = result.get("explanation_type", "unknown")
    base_value = result.get("base_value", None)

    st.success("Prediction completed")

    col1, col2, col3 = st.columns(3)
    col1.metric("Churn Prediction", "Yes" if churn_prediction == 1 else "No")
    col2.metric("Churn Probability", f"{churn_probability * 100:.2f}%")
    col3.metric("Risk Level", risk_level)

    st.caption(f"Model default prediction: {'Yes' if model_prediction == 1 else 'No'}")
    st.caption(f"Threshold-adjusted prediction: {'Yes' if churn_prediction == 1 else 'No'}")
    st.caption(f"Explanation type: {explanation_type}")

    if base_value is not None:
        st.caption(f"SHAP base value: {base_value}")

    st.progress(max(0.0, min(float(churn_probability), 1.0)))

    st.write("**Recommended Retention Action**")
    st.info(retention_action)

    if top_drivers:
        st.write("**Top Model Drivers (SHAP)**")
        for driver in top_drivers:
            direction_icon = "↑" if driver.get("direction") == "increase" else "↓"
            direction_label = "Increases churn risk" if driver.get("direction") == "increase" else "Reduces churn risk"

            st.markdown(
                f"""
**{direction_icon} {driver.get('title', 'Unknown Feature')}**  
- Value: `{driver.get('value', 'N/A')}`  
- SHAP Value: `{driver.get('shap_value', 0)}`  
- Impact: **{driver.get('impact', 'Unknown')}**  
- {direction_label}  
- {driver.get('description', '')}
"""
            )

    explanation_df = safe_dataframe(explanation_bars)
    if not explanation_df.empty:
        st.write("**SHAP Explanation Bars**")
        st.dataframe(explanation_df, use_container_width=True)
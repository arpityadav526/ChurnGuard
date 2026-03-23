import streamlit as st
import pandas as pd
from components.helpers import post_file, safe_dataframe

st.title("Batch Churn Prediction")

required_columns = [
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

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        preview_df = pd.read_csv(uploaded_file)

        if preview_df.empty:
            st.error("Uploaded CSV is empty.")
            st.stop()

        missing_cols = [col for col in required_columns if col not in preview_df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {missing_cols}")
            st.stop()

        st.subheader("Uploaded File Preview")
        st.dataframe(preview_df.head(), use_container_width=True)

    except Exception:
        st.error("Could not read the uploaded CSV.")
        st.stop()

    if st.button("Run Batch Prediction"):
        with st.spinner("Processing batch predictions..."):
            result = post_file("/predict-batch", uploaded_file)

        if result is None:
            st.stop()

        st.success("Batch prediction completed")

        col1, col2 = st.columns(2)
        col1.metric("Total Rows", result.get("total_rows", 0))
        col2.metric("High Risk Customers", result.get("high_risk_count", 0))

        predictions = result.get("predictions", [])
        result_df = safe_dataframe(predictions)

        if not result_df.empty:
            st.subheader("Prediction Results")
            st.dataframe(result_df, use_container_width=True)

            csv_data = result_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Predictions CSV",
                data=csv_data,
                file_name="batch_predictions.csv",
                mime="text/csv"
            )
        else:
            st.warning("No predictions returned.")
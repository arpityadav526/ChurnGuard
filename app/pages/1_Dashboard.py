import streamlit as st
import pandas as pd
import requests
from components.helpers import get_data, safe_dataframe, BASE_URL

st.write("BASE_URL in app:", BASE_URL)

# direct backend checks
try:
    health_resp = requests.get(f"{BASE_URL}/health", timeout=30)
    st.write("Health status code:", health_resp.status_code)
    st.json(health_resp.json())
except Exception as e:
    st.error(f"Direct /health request failed: {e}")

try:
    metrics_resp = requests.get(f"{BASE_URL}/metrics", timeout=30)
    st.write("Metrics status code:", metrics_resp.status_code)
    try:
        st.json(metrics_resp.json())
    except Exception:
        st.write(metrics_resp.text)
except Exception as e:
    st.error(f"Direct /metrics request failed: {e}")

st.title("Dashboard")

with st.spinner("Loading dashboard data..."):
    metrics = get_data("/metrics")
    risk_distribution = get_data("/risk-distribution")
    contract_churn = get_data("/contract-churn")
    payment_method_churn = get_data("/payment-method-churn")
    recent_predictions = get_data("/recent-predictions")

# Error check for main metrics
if metrics is None:
    st.error("Failed to load metrics from backend")
    st.stop()

# Top metrics
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", metrics.get("total_customers", 0))
col2.metric("Churn Rate", f"{metrics.get('churn_rate', 0)}%")
col3.metric("High Risk Customers", metrics.get("high_risk_customers", 0))
col4.metric("Revenue At Risk", f"${metrics.get('predicted_revenue_at_risk', 0):,.2f}")
col5.metric("Predictions Made", metrics.get("total_predictions_made", 0))

st.markdown("---")

col_left, col_right = st.columns(2)

# Risk Distribution
with col_left:
    st.subheader("Risk Distribution")
    if risk_distribution:
        risk_df = pd.DataFrame({
            "Risk Level": risk_distribution.get("labels", []),
            "Count": risk_distribution.get("values", [])
        })
        if not risk_df.empty:
            st.bar_chart(risk_df.set_index("Risk Level"))
        else:
            st.info("No risk data available")

# Contract Churn
with col_right:
    st.subheader("Contract-wise Churn Rate")
    contract_df = safe_dataframe(contract_churn)
    if not contract_df.empty:
        contract_df = contract_df.rename(
            columns={"Contract": "Contract Type", "churn_rate": "Churn Rate"}
        )
        st.dataframe(contract_df, use_container_width=True)
        st.bar_chart(contract_df.set_index("Contract Type")[["Churn Rate"]])
    else:
        st.info("No contract churn data available")

st.markdown("---")

# Payment Method
st.subheader("Payment Method Churn Rate")
payment_df = safe_dataframe(payment_method_churn)
if not payment_df.empty:
    payment_df = payment_df.rename(
        columns={"PaymentMethod": "Payment Method", "churn_rate": "Churn Rate"}
    )
    st.dataframe(payment_df, use_container_width=True)
else:
    st.info("No payment method data available")

st.markdown("---")

# Recent Predictions
st.subheader("Recent Predictions")
recent_df = safe_dataframe(recent_predictions)
if not recent_df.empty:
    st.dataframe(recent_df, use_container_width=True)
else:
    st.info("No recent predictions found yet.")
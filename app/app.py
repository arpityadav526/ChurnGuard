


import streamlit as st



st.set_page_config(
    page_title="ChurnGuard Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title("ChurnGaurd")
st.subheader("Customer Churn Analytics Platform")

st.markdown("""
Welcome to **ChurnGuard**.

Use the sidebar to navigate through:
- Dashboard
- Single Customer Prediction
- Batch Prediction
- Model Insights
""")
st.info("Make sure the FastAPI backend is running on http://127.0.0.1:8000")
import streamlit as st
from components.helpers import get_data, safe_dataframe

st.title("Prediction History")

with st.spinner("Loading prediction history..."):
    data = get_data("/recent-predictions?limit=50")

if data is None:
    st.error("Failed to load prediction history.")
    st.stop()

history_df = safe_dataframe(data)

if history_df.empty:
    st.info("No prediction history found yet.")
else:
    st.dataframe(history_df, use_container_width=True)
import streamlit as st
import pandas as pd
from components.helpers import get_data

st.title("Model Performance")

with st.spinner("Loading model performance metrics..."):
    performance = get_data("/model-performance")

if performance is None:
    st.error("Failed to load model performance data.")
    st.stop()

accuracy = performance.get("accuracy", 0.0)
precision = performance.get("precision", 0.0)
recall = performance.get("recall", 0.0)
f1_score = performance.get("f1_score", 0.0)
roc_auc = performance.get("roc_auc", 0.0)

cm = performance.get("confusion_matrix", {})
tn = cm.get("tn", 0)
fp = cm.get("fp", 0)
fn = cm.get("fn", 0)
tp = cm.get("tp", 0)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Accuracy", f"{accuracy * 100:.2f}%")
col2.metric("Precision", f"{precision * 100:.2f}%")
col3.metric("Recall", f"{recall * 100:.2f}%")
col4.metric("F1 Score", f"{f1_score * 100:.2f}%")
col5.metric("ROC-AUC", f"{roc_auc * 100:.2f}%")

st.markdown("---")

st.subheader("Confusion Matrix")

cm_df = pd.DataFrame(
    [[tn, fp], [fn, tp]],
    index=["Actual No Churn", "Actual Churn"],
    columns=["Predicted No Churn", "Predicted Churn"]
)

st.dataframe(cm_df, use_container_width=True)

st.markdown("---")

st.subheader("Metric Summary")

summary_df = pd.DataFrame({
    "Metric": ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"],
    "Score": [accuracy, precision, recall, f1_score, roc_auc]
})

st.dataframe(summary_df, use_container_width=True)
st.bar_chart(summary_df.set_index("Metric")[["Score"]])

st.markdown("---")

st.info(
    "These metrics summarize the churn model's predictive quality. "
    "Accuracy shows overall correctness, precision reflects how many predicted churners were correct, "
    "recall shows how many actual churners were captured, F1 balances precision and recall, "
    "and ROC-AUC reflects ranking quality across thresholds."
)
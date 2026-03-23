import streamlit as st
from components.helpers import get_data, safe_dataframe

st.title("Customer Insights")

tab1, tab2, tab3 = st.tabs(["Latest Customer", "Customer by Index", "Feature Importance"])

with tab1:
    st.subheader("Latest Predicted Customer")

    with st.spinner("Loading latest customer insights..."):
        latest_data = get_data("/insights/latest-customer")

    if latest_data is None:
        st.error("Failed to load latest customer insights")
    elif "message" in latest_data:
        st.info(latest_data["message"])
    else:
        profile = latest_data.get("customer_profile", {})

        col1, col2, col3 = st.columns(3)
        col1.metric("Risk Level", latest_data.get("risk_level", "Unknown"))
        col2.metric(
            "Churn Prediction",
            "Yes" if latest_data.get("churn_prediction", 0) == 1 else "No"
        )
        col3.metric(
            "Churn Probability",
            f"{latest_data.get('churn_probability', 0) * 100:.2f}%"
        )

        st.write("**Customer Profile**")
        st.json(profile)

        st.write("**Retention Action**")
        st.info(latest_data.get("retention_action", "No action"))

        top_drivers = latest_data.get("top_drivers", [])
        if top_drivers:
            st.write("**Top Drivers**")
            for driver in top_drivers:
                st.write(
                    f"- **{driver['title']}**: {driver['description']} ({driver['impact']})"
                )

        explanation_bars = latest_data.get("explanation_bars", [])
        explanation_df = safe_dataframe(explanation_bars)
        if not explanation_df.empty:
            st.write("**Explanation Bars**")
            st.dataframe(explanation_df, use_container_width=True)

with tab2:
    st.subheader("Fetch Customer by Prediction History Index")
    index = st.number_input("Enter customer index", min_value=0, value=0, step=1)

    if st.button("Get Customer Insights"):
        with st.spinner("Loading customer insights..."):
            customer_data = get_data(f"/insights/customer?index={index}")

        if customer_data is None:
            st.error("Failed to load customer insights")
        elif "message" in customer_data:
            st.info(customer_data["message"])
        else:
            profile = customer_data.get("customer_profile", {})

            col1, col2, col3 = st.columns(3)
            col1.metric("Risk Level", customer_data.get("risk_level", "Unknown"))
            col2.metric(
                "Churn Prediction",
                "Yes" if customer_data.get("churn_prediction", 0) == 1 else "No"
            )
            col3.metric(
                "Churn Probability",
                f"{customer_data.get('churn_probability', 0) * 100:.2f}%"
            )

            st.write("**Customer Profile**")
            st.json(profile)

            st.write("**Retention Action**")
            st.info(customer_data.get("retention_action", "No action"))

            top_drivers = customer_data.get("top_drivers", [])
            if top_drivers:
                st.write("**Top Drivers**")
                for driver in top_drivers:
                    st.write(
                        f"- **{driver['title']}**: {driver['description']} ({driver['impact']})"
                    )

            explanation_bars = customer_data.get("explanation_bars", [])
            explanation_df = safe_dataframe(explanation_bars)
            if not explanation_df.empty:
                st.write("**Explanation Bars**")
                st.dataframe(explanation_df, use_container_width=True)

with tab3:
    st.subheader("Global Feature Importance")

    with st.spinner("Loading feature importance..."):
        feature_importance = get_data("/insights/feature-importance")

    if feature_importance is None:
        st.error("Failed to load feature importance")
    else:
        fi_df = safe_dataframe(feature_importance)
        if not fi_df.empty:
            st.dataframe(fi_df, use_container_width=True)

            if "feature" in fi_df.columns and "score" in fi_df.columns:
                st.bar_chart(fi_df.set_index("feature")[["score"]])
        else:
            st.info("No feature importance data available")
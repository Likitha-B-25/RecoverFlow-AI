import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="RecoverFlow AI",
    page_icon="💳",
    layout="wide"
)

st.title("💳 RecoverFlow AI")
st.subheader("Intelligent Payment Failure Recovery Agent")

st.divider()

st.write("""
Welcome to RecoverFlow AI.

This dashboard analyzes failed payments, identifies recovery opportunities,
prioritizes recovery actions, and provides intelligent retry decisions.
""")

st.subheader("Payment Analysis")

sample_data = {
    "payments": [
        {
            "payment_id": "PAY001",
            "amount": 5000,
            "status": "failed",
            "failure_reason": "temporary bank issue",
            "retry_count": 1
        },
        {
            "payment_id": "PAY002",
            "amount": 2500,
            "status": "success",
            "failure_reason": None,
            "retry_count": 0
        },
        {
            "payment_id": "PAY003",
            "amount": 7500,
            "status": "failed",
            "failure_reason": "insufficient funds",
            "retry_count": 3
        },
        {
            "payment_id": "PAY004",
            "amount": 3000,
            "status": "failed",
            "failure_reason": "expired payment method",
            "retry_count": 0
        },
        {
            "payment_id": "PAY005",
            "amount": 1000,
            "status": "failed",
            "failure_reason": "repeated failure",
            "retry_count": 2
        }
    ]
}

if st.button("🚀 Analyze Payments", use_container_width=True):

    try:
        response = requests.post(
            "http://127.0.0.1:8000/analyze-payments",
            json=sample_data
        )

        if response.status_code == 200:

            result = response.json()

            st.success("Payment analysis completed successfully!")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Payments",
                result["total_payments"]
            )

            col2.metric(
                "Failed Payments",
                result["failed_payments"]
            )

            col3.metric(
                "Revenue at Risk",
                f"₹{result['revenue_at_risk']:,}"
            )

            st.divider()

            st.subheader("Recovery Analysis")

            analysis = result["recovery_analysis"]

            df = pd.DataFrame(analysis)

            st.dataframe(
                df,
                use_container_width=True
            )

            st.subheader("Detailed Agent Decisions")

            for payment in analysis:

                with st.expander(
                    f"{payment['payment_id']} - ₹{payment['amount']:,}"
                ):
                    st.write(
                        "Failure Reason:",
                        payment["failure_reason"]
                    )

                    st.write(
                        "Recovery Probability:",
                        f"{payment['recovery_probability']}%"
                    )

                    st.write(
                        "Priority Score:",
                        payment["priority_score"]
                    )

                    st.write(
                        "Priority Level:",
                        payment["priority_level"]
                    )

                    st.write(
                        "Recommended Action:",
                        payment["recommended_action"]
                    )

                    st.write(
                        "Agent Decision:",
                        payment["agent_decision"]
                    )

        else:
            st.error(
                f"Backend returned an error: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to the FastAPI backend. "
            "Make sure Uvicorn is running on port 8000."
        )
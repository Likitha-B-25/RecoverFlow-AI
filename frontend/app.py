import requests
import streamlit as st
import pandas as pd


# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="RecoverFlow AI",
    page_icon="💳",
    layout="wide"
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("💳 RecoverFlow AI")
st.subheader("Intelligent Payment Failure Recovery Agent")

st.write(
    "RecoverFlow AI analyzes failed payments, estimates recovery opportunities, "
    "prioritizes revenue at risk, and executes bounded recovery actions."
)

st.divider()


# ---------------------------------------------------------
# Payment Recovery Dashboard
# ---------------------------------------------------------

st.header("💰 Payment Recovery Dashboard")


if st.button("🚀 Analyze Payments", use_container_width=True):

    sample_payments = {
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

    try:

        response = requests.post(
            f"{API_URL}/analyze-payments",
            json=sample_payments,
            timeout=10
        )

        if response.status_code == 200:

            result = response.json()

            st.session_state["analysis"] = result

        else:

            st.error(
                f"Backend returned HTTP {response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to FastAPI. "
            "Make sure the backend is running on port 8000."
        )

    except Exception as e:

        st.error(
            f"Unexpected error: {e}"
        )


# ---------------------------------------------------------
# Display Analysis
# ---------------------------------------------------------

if "analysis" in st.session_state:

    result = st.session_state["analysis"]

    st.success(
        "Payment analysis completed successfully!"
    )


    # -----------------------------------------------------
    # Dashboard Metrics
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

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
        f"₹{result['revenue_at_risk']:,.2f}"
    )

    col4.metric(
        "Potential Recoverable",
        f"₹{result['potential_recoverable_revenue']:,.2f}"
    )


    st.divider()


    # -----------------------------------------------------
    # Recovery Analysis
    # -----------------------------------------------------

    st.header("📊 Recovery Analysis")

    analysis = result["recovery_analysis"]

    df = pd.DataFrame(analysis)

    display_columns = [
        "payment_id",
        "amount",
        "failure_reason",
        "retry_count",
        "recovery_probability",
        "priority_score",
        "priority_level",
        "recommended_action",
        "should_retry"
    ]

    st.dataframe(
        df[display_columns],
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # -----------------------------------------------------
    # Agent Recovery Decisions
    # -----------------------------------------------------

    st.header("🤖 Agent Recovery Decisions")


    for payment in analysis:

        with st.expander(
            f"{payment['payment_id']} — ₹{payment['amount']:,.2f}"
        ):

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Recovery Probability",
                f"{payment['recovery_probability']}%"
            )

            col2.metric(
                "Expected Recovery",
                f"₹{payment['priority_score']:,.2f}"
            )

            col3.metric(
                "Priority",
                payment["priority_level"].upper()
            )


            st.write(
                f"**Diagnosis:** {payment['diagnosis']}"
            )

            st.write(
                f"**Recommended Action:** "
                f"`{payment['recommended_action']}`"
            )

            st.write(
                f"**Agent Decision:** "
                f"{payment['agent_decision']}"
            )


            # -------------------------------------------------
            # Retry Decision
            # -------------------------------------------------

            if payment["should_retry"]:

                st.info(
                    f"Automatic retry permitted after "
                    f"{payment['retry_after_hours']} hours."
                )

            else:

                st.warning(
                    "Automatic retry is not permitted."
                )


            # -------------------------------------------------
            # Execute Recovery Action
            # -------------------------------------------------

            if st.button(
                f"⚡ Execute {payment['payment_id']} Recovery",
                key=f"execute_{payment['payment_id']}"
            ):

                try:

                    execution_response = requests.post(

                        f"{API_URL}/execute-recovery",

                        json={
                            "payment_id": payment["payment_id"],
                            "action": payment["recommended_action"],
                            "amount": payment["amount"],
                            "reason": payment["diagnosis"],

                            # Important safety information
                            "retry_count": payment["retry_count"]
                        },

                        timeout=10
                    )


                    if execution_response.status_code == 200:

                        execution_result = execution_response.json()

                        status = execution_result.get(
                            "status"
                        )


                        # Successful demo execution
                        if status == "executed":

                            st.success(
                                "✅ Recovery action executed successfully "
                                "in demo mode."
                            )


                        # Maximum retry / manual review
                        elif status == "escalated":

                            st.warning(
                                "⚠️ Payment escalated for manual review."
                            )


                            if execution_result.get("message"):

                                st.info(
                                    execution_result["message"]
                                )


                        # Blocked action
                        elif status == "blocked":

                            st.error(
                                "🛑 Recovery action blocked."
                            )


                            if execution_result.get("reason"):

                                st.info(
                                    execution_result["reason"]
                                )


                        else:

                            st.error(
                                "Unexpected recovery response."
                            )


                    else:

                        st.error(
                            f"Execution failed: "
                            f"HTTP {execution_response.status_code}"
                        )


                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to the recovery backend. "
                        "Make sure FastAPI is running."
                    )


                except Exception as e:

                    st.error(
                        f"Recovery execution error: {e}"
                    )


    st.divider()


    # ---------------------------------------------------------
    # Recovery Audit Trail
    # ---------------------------------------------------------

    st.header("🧾 Recovery Audit Trail")


    try:

        audit_response = requests.get(
            f"{API_URL}/audit-log",
            timeout=10
        )


        if audit_response.status_code == 200:

            audit_result = audit_response.json()

            total_actions = audit_result.get(
                "total_actions",
                0
            )


            if total_actions == 0:

                st.info(
                    "No recovery actions have been executed yet."
                )

            else:

                st.success(
                    f"{total_actions} "
                    f"recovery action(s) recorded."
                )


                audit_df = pd.DataFrame(
                    audit_result.get(
                        "audit_log",
                        []
                    )
                )


                if not audit_df.empty:

                    st.dataframe(
                        audit_df,
                        use_container_width=True,
                        hide_index=True
                    )


        else:

            st.error(
                f"Audit log request failed: "
                f"HTTP {audit_response.status_code}"
            )


    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to the audit log backend."
        )

    except Exception as e:

        st.error(
            f"Could not load audit trail: {e}"
        )


    st.divider()


    # ---------------------------------------------------------
    # Recovery Controls
    # ---------------------------------------------------------

    st.header("🛡️ Recovery Controls")


    controls = [

        "Maximum retry limit: 3 attempts",

        "Repeated failures are escalated for manual review",

        "Expired payment methods use payment-link recovery",

        "Temporary failures may be retried after a delay",

        "Every recovery action is recorded in the audit trail",

        "Recovery execution is simulated safely in demo mode"

    ]


    for control in controls:

        st.write(
            f"✅ {control}"
        )
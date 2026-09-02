from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional


app = FastAPI(
    title="RecoverFlow AI",
    description="Intelligent Payment Failure Recovery Agent",
    version="1.0.0"
)


class Payment(BaseModel):
    payment_id: str
    amount: float
    status: str
    failure_reason: Optional[str] = None
    retry_count: int = 0


class PaymentBatch(BaseModel):
    payments: List[Payment]


def get_recovery_probability(payment: Payment) -> int:
    """Calculate recovery probability based on failure reason."""

    reason = (payment.failure_reason or "").lower()

    probability_map = {
        "temporary bank issue": 85,
        "network timeout": 80,
        "insufficient funds": 65,
        "expired payment method": 45,
        "repeated failure": 20
    }

    return probability_map.get(reason, 40)


def calculate_priority(amount: float, probability: int) -> float:
    """Calculate expected recoverable value."""

    return round(amount * probability / 100, 2)


def get_priority_level(priority_score: float) -> str:

    if priority_score >= 5000:
        return "high"

    elif priority_score >= 2000:
        return "medium"

    return "low"


def diagnose_payment(payment: Payment):

    reason = (payment.failure_reason or "").lower()

    if reason in ["temporary bank issue", "network timeout"]:
        return {
            "diagnosis": reason or "temporary technical issue",
            "recommended_action": "retry_payment",
            "retry_after_hours": 2
        }

    elif reason == "insufficient funds":
        return {
            "diagnosis": "insufficient funds",
            "recommended_action": "retry_payment",
            "retry_after_hours": 24
        }

    elif reason == "expired payment method":
        return {
            "diagnosis": "expired payment method",
            "recommended_action": "send_payment_link",
            "retry_after_hours": None
        }

    elif reason == "repeated failure":
        return {
            "diagnosis": "repeated payment failure",
            "recommended_action": "manual_review",
            "retry_after_hours": None
        }

    return {
        "diagnosis": reason or "unknown failure",
        "recommended_action": "send_payment_reminder",
        "retry_after_hours": None
    }


def get_agent_decision(payment: Payment, recommended_action: str):

    max_retries = 3

    # Payment does not need a retry
    if recommended_action != "retry_payment":
        return {
            "max_retries": max_retries,
            "should_retry": False,
            "agent_decision": f"Do not retry. Recommended action: {recommended_action}"
        }

    # Maximum retries reached
    if payment.retry_count >= max_retries:
        return {
            "max_retries": max_retries,
            "should_retry": False,
            "agent_decision": "Maximum retry limit reached. Send for manual review."
        }

    # Retry is allowed
    return {
        "max_retries": max_retries,
        "should_retry": True,
        "agent_decision": f"Retry allowed. Attempt {payment.retry_count + 1} of {max_retries}."
    }


@app.get("/")
def home():
    return {
        "message": "Welcome to RecoverFlow AI",
        "status": "Backend is running successfully"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/analyze-payments")
def analyze_payments(batch: PaymentBatch):

    failed_payments = [
        payment for payment in batch.payments
        if payment.status.lower() == "failed"
    ]

    revenue_at_risk = sum(
        payment.amount for payment in failed_payments
    )

    analyzed_payments = []

    for payment in failed_payments:

        diagnosis_result = diagnose_payment(payment)

        recovery_probability = get_recovery_probability(payment)

        priority_score = calculate_priority(
            payment.amount,
            recovery_probability
        )

        priority_level = get_priority_level(priority_score)

        agent_result = get_agent_decision(
            payment,
            diagnosis_result["recommended_action"]
        )

        analyzed_payments.append({
            "payment_id": payment.payment_id,
            "amount": payment.amount,
            "failure_reason": payment.failure_reason,
            "retry_count": payment.retry_count,
            "recovery_probability": recovery_probability,
            "priority_score": priority_score,
            "priority_level": priority_level,
            **diagnosis_result,
            **agent_result
        })

    # Highest priority payments appear first
    analyzed_payments.sort(
        key=lambda payment: payment["priority_score"],
        reverse=True
    )

    return {
        "total_payments": len(batch.payments),
        "failed_payments": len(failed_payments),
        "revenue_at_risk": revenue_at_risk,
        "recovery_analysis": analyzed_payments
    }
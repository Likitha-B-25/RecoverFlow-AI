# RecoverFlow AI 💳

## Intelligent Payment Failure Recovery Agent

RecoverFlow AI is an intelligent payment revenue recovery agent built for the **Razorpay AI Buildathon — Track 3: AI Revenue Recovery**.

The system analyzes failed payments, estimates recovery opportunities, prioritizes revenue at risk, recommends recovery actions, executes bounded recovery workflows in safe demo mode, and maintains an audit trail.

---

## 🎯 Problem

Failed payments create revenue leakage for businesses. Different payment failures require different recovery strategies.

For example:

- Temporary bank failures can be retried later.
- Network timeouts can be retried after a delay.
- Insufficient funds may require a later retry.
- Expired payment methods require a payment link.
- Repeated failures should be escalated for manual review.

---

## 💡 Solution

RecoverFlow AI automatically analyzes failed payments and selects an appropriate recovery strategy.

### Workflow

Failed Payment
↓
Failure Diagnosis
↓
Recovery Probability
↓
Expected Recoverable Value
↓
Priority Scoring
↓
Agent Decision
↓
Bounded Recovery Action
↓
Demo Execution
↓
Audit Trail

---

## 🚀 Key Features

### Payment Analysis

- Analyze payment batches
- Identify failed payments
- Identify failure reasons
- Calculate revenue at risk
- Estimate potential recoverable revenue

### Intelligent Recovery Decisions

- Calculate recovery probability
- Calculate expected recovery value
- Prioritize high-value recovery opportunities
- Recommend recovery actions
- Generate explainable agent decisions

### Bounded Recovery

- Maximum automatic retry limit of 3 attempts
- Prevent unlimited retries
- Escalate repeated failures
- Delay temporary-failure retries
- Use payment links for expired payment methods

### Recovery Execution

Supported recovery actions:

- `retry_payment`
- `send_payment_link`
- `manual_review`
- `send_payment_reminder`

Recovery execution is performed in safe demo mode.

No real customer payment is processed by this project.

### Audit Trail

Recovery actions are recorded with:

- Timestamp
- Payment ID
- Amount
- Recovery action
- Reason
- Execution status

---

## 📊 Example

For the included sample payment batch:

- Total Payments: **5**
- Failed Payments: **4**
- Revenue at Risk: **₹16,500**
- Potential Recoverable Revenue: **₹10,675**

Potential recoverable revenue is a modeled estimate based on recovery probability. It is not a claim of actual money recovered.

### Example Decisions

| Payment | Amount | Failure Reason | Probability | Expected Recovery | Action |
|---|---:|---|---:|---:|---|
| PAY001 | ₹5,000 | Temporary bank issue | 85% | ₹4,250 | Retry payment |
| PAY003 | ₹7,500 | Insufficient funds | 65% | ₹4,875 | Manual review after retry limit |
| PAY004 | ₹3,000 | Expired payment method | 45% | ₹1,350 | Send payment link |
| PAY005 | ₹1,000 | Repeated failure | 20% | ₹200 | Manual review |

---

## 🤖 Agent Decision Logic

The agent evaluates:

1. Failure reason
2. Payment amount
3. Retry count
4. Recovery probability
5. Expected recovery value
6. Priority score

Expected recovery is calculated as:

`Payment Amount × Recovery Probability`

The system then selects an appropriate recovery action.

---

## 🛡️ Safety Controls

### Retry Limit

Maximum automatic retries: **3**

When the retry limit is reached:

**Automatic Retry → Blocked**

**Payment → Manual Review**

### Failure-Specific Actions

| Failure | Recovery Action |
|---|---|
| Temporary Bank Issue | Delayed Retry |
| Network Timeout | Delayed Retry |
| Insufficient Funds | Delayed Retry |
| Expired Payment Method | Payment Link |
| Repeated Failure | Manual Review |

---

## 🧾 Auditability

Every recovery action is recorded so that agent decisions can be reviewed later.

Example:

**Payment:** PAY003  
**Action:** manual_review  
**Status:** escalated  
**Reason:** Maximum retry limit reached

---

## 🏗️ System Architecture

Streamlit Dashboard
↓
FastAPI Backend
↓
Payment Analysis
↓
Recovery Decision Agent
↓
Bounded Recovery Workflow
↓
Audit Trail

---

## 🛠️ Technology Stack

- Python
- FastAPI
- Uvicorn
- Streamlit
- Pandas
- Pydantic
- Requests

---

## 📁 Project Structure

```text
RecoverFlow-AI/
│
├── backend/
│   └── app/
│       └── main.py
│
├── frontend/
│   └── app.py
│
├── data/
├── models/
├── requirements.txt
├── .gitignore
└── README.md
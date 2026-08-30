\# TrustBridge 🤝



\### AI-Powered Alternative Trust \& Credit Scoring Platform



TrustBridge is an AI/ML-powered platform designed to estimate an applicant's \*\*trust and creditworthiness using alternative digital and community signals\*\*, especially for individuals who may have limited or no traditional credit history.



Instead of relying entirely on formal bank statements or credit bureau records, TrustBridge analyzes everyday financial and behavioral signals such as UPI activity, payment regularity, savings growth, peer vouches, business vintage, geographic stability, and digital footprint diversity.



\---



\## 🚀 Features



\* 🧠 \*\*Machine Learning Trust Scoring\*\*



&#x20; \* Logistic Regression-based scoring model

&#x20; \* Converts applicant signals into a trust score from 0–100



\* 📊 \*\*Explainable AI\*\*



&#x20; \* Shows which signals positively or negatively influence the score

&#x20; \* Provides a plain-language explanation of the result



\* 👤 \*\*Demo Personas\*\*



&#x20; \* Vegetable Cart Vendor

&#x20; \* Food Delivery Rider

&#x20; \* Smallholder Farmer

&#x20; \* New Applicant / Thin Signal History



\* 💳 \*\*Financial Product Recommendations\*\*



&#x20; \* Individual micro-loan

&#x20; \* Starter micro-loan

&#x20; \* Inventory BNPL

&#x20; \* Savings-linked credit

&#x20; \* Group-guaranteed micro-loans



\* ⚡ \*\*FastAPI Backend\*\*



&#x20; \* REST API for scoring applicants

&#x20; \* Persona endpoints

&#x20; \* Model information endpoint



\* 💻 \*\*Modern Frontend\*\*



&#x20; \* Interactive applicant scoring interface

&#x20; \* Real-time communication with the backend



\---



\## 🧠 How TrustBridge Works



```text

Applicant Signals

&#x20;      │

&#x20;      ▼

┌──────────────────────────────┐

│   Feature Extraction         │

│                              │

│ • UPI Activity               │

│ • Transaction Regularity     │

│ • Monthly Inflow             │

│ • Recharge Regularity        │

│ • Utility Payments           │

│ • Savings Growth             │

│ • Peer Vouches               │

│ • Business Vintage           │

│ • Geographic Stability       │

│ • Digital Footprint          │

└──────────────┬───────────────┘

&#x20;              │

&#x20;              ▼

&#x20;      Feature Scaling

&#x20;              │

&#x20;              ▼

&#x20;    Logistic Regression

&#x20;         ML Model

&#x20;              │

&#x20;              ▼

&#x20;      Trust Probability

&#x20;              │

&#x20;              ▼

&#x20;       Trust Score 0–100

&#x20;              │

&#x20;      ┌───────┴────────┐

&#x20;      ▼                ▼

&#x20;Explainability    Recommendation

&#x20;      │                │

&#x20;      └───────┬────────┘

&#x20;              ▼

&#x20;        User Dashboard

```



\---



\## 📈 Trust Score Tiers



| Score       | Tier              | Recommendation                                 |

| ----------- | ----------------- | ---------------------------------------------- |

| \*\*72–100\*\*  | 🟢 High Trust     | Standard micro-loan limits                     |

| \*\*48–71.9\*\* | 🟡 Building Trust | Starter loan / savings-linked credit           |

| \*\*0–47.9\*\*  | 🟠 Emerging       | Savings product or group-guaranteed micro-loan |



\---



\## 🔍 Signals Used



TrustBridge currently uses 10 alternative signals:



| Signal                        | Description                    |

| ----------------------------- | ------------------------------ |

| `upi\_txn\_frequency`           | Frequency of UPI transactions  |

| `upi\_txn\_regularity`          | Consistency of UPI activity    |

| `avg\_monthly\_inflow`          | Average monthly digital inflow |

| `recharge\_regularity`         | Regularity of mobile recharges |

| `utility\_payment\_timeliness`  | Timeliness of utility payments |

| `savings\_growth\_6m`           | Savings growth over six months |

| `peer\_vouches`                | Community/peer trust signals   |

| `business\_vintage\_months`     | Length of business activity    |

| `geo\_stability`               | Geographic/location stability  |

| `digital\_footprint\_diversity` | Diversity of digital activity  |



\---



\## 🛠️ Tech Stack



\### Backend



\* Python

\* FastAPI

\* Uvicorn

\* Scikit-learn

\* NumPy

\* Joblib

\* Pydantic



\### Frontend



\* JavaScript

\* React / Vite

\* HTML

\* CSS



\### Machine Learning



\* Logistic Regression

\* Feature Scaling

\* Model-based probability scoring

\* Feature contribution analysis



\---



\## 📁 Project Structure



```text

trustbridge/

│

├── backend/

│   ├── app.py

│   ├── model.joblib

│   ├── scaler.joblib

│   ├── feature\_meta.json

│   ├── requirements.txt

│   └── .venv/

│

├── frontend/

│   ├── package.json

│   ├── src/

│   ├── public/

│   └── ...

│

├── .gitignore

└── README.md

```



> `.venv/` and `node\_modules/` should not be committed to GitHub.



\---



\# ⚙️ Installation



\## Prerequisites



Make sure you have installed:



\* Python 3.11

\* Node.js

\* npm

\* Git



\---



\## 1. Clone the Repository



```bash

git clone https://github.com/YOUR\_USERNAME/trustbridge.git

cd trustbridge

```



\---



\# 🐍 Backend Setup



Navigate to the backend:



```powershell

cd backend

```



Create a Python 3.11 virtual environment:



```powershell

py -3.11 -m venv .venv

```



Activate it:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



Upgrade pip:



```powershell

python -m pip install --upgrade pip

```



Install dependencies:



```powershell

python -m pip install -r requirements.txt

```



Start the API:



```powershell

python -m uvicorn app:app --reload --port 8000

```



The backend will run at:



```text

http://127.0.0.1:8000

```



\---



\# 💻 Frontend Setup



Open another terminal.



Navigate to the frontend:



```powershell

cd frontend

```



Install dependencies:



```powershell

npm install

```



Start the development server:



```powershell

npm run dev

```



The frontend will normally be available at:



```text

http://localhost:5173

```



\---



\# 🔌 API Endpoints



\## Health Check



```http

GET /

```



Returns the API status.



\---



\## List Demo Personas



```http

GET /personas

```



Returns the available demo applicants.



\---



\## Score a Demo Persona



```http

GET /score/persona/{persona\_key}

```



Example:



```text

GET /score/persona/vendor

```



Available personas:



```text

vendor

gig\_worker

farmer

risky\_applicant

```



\---



\## Score a Custom Applicant



```http

POST /score

```



Example request:



```json

{

&#x20; "upi\_txn\_frequency": 24,

&#x20; "upi\_txn\_regularity": 72,

&#x20; "avg\_monthly\_inflow": 16000,

&#x20; "recharge\_regularity": 68,

&#x20; "utility\_payment\_timeliness": 80,

&#x20; "savings\_growth\_6m": 12,

&#x20; "peer\_vouches": 3,

&#x20; "business\_vintage\_months": 48,

&#x20; "geo\_stability": 85,

&#x20; "digital\_footprint\_diversity": 55,

&#x20; "name": "Applicant"

}

```



The API returns:



\* Trust score

\* Trust tier

\* Recommended financial product

\* Suggested amount

\* Feature contributions

\* Plain-language explanation



\---



\## Model Information



```http

GET /model-info

```



Returns model validation information and feature metadata.



\---



\# 🤖 Explainable AI



TrustBridge does not only produce a score.



It also calculates the contribution of individual features to the result.



For each signal, the system provides:



```text

Feature

Label

Raw Value

Impact

```



This makes the model output easier to understand and helps users identify the factors that are contributing positively or negatively to the applicant's trust score.



\---



\# 👥 Demo Personas



\### Radha — Vegetable Cart Vendor



Represents a small informal business with consistent digital transactions and strong payment behavior.



\### Aman — Food Delivery Rider



Represents a gig worker with moderate digital activity and variable income stability.



\### Suresh — Smallholder Farmer



Represents a user with lower digital transaction frequency but strong business vintage and geographic stability.



\### New Applicant — Thin Signal History



Represents an applicant with limited digital history and weaker trust signals.



\---



\# 🔐 Responsible AI \& Privacy



TrustBridge is a prototype intended for experimentation and demonstration.



The current model uses synthetic/demo data and should \*\*not\*\* be used to make real-world lending decisions without appropriate validation, consent, privacy controls, fairness testing, regulatory review, and production-grade security.



The project is designed around the idea that alternative signals can potentially help underserved individuals build a financial identity, while recognizing that alternative-data systems can introduce privacy and fairness risks.



\---



\# 📊 Current Model



The current implementation uses:



```text

Logistic Regression

&#x20;       +

Feature Scaling

&#x20;       +

Alternative Financial Signals

&#x20;       ↓

Trust Probability

&#x20;       ↓

Trust Score

```



The model artifacts are stored as:



```text

backend/model.joblib

backend/scaler.joblib

```



Model metadata is stored in:



```text

backend/feature\_meta.json

```



\---



\# 🔮 Future Scope



\* Real consented transaction data integration

\* UPI/payment data connectors

\* Improved model calibration

\* Fairness and bias auditing

\* SHAP-based explainability

\* Fraud/anomaly detection

\* Time-series behavioral analysis

\* Multilingual user interface

\* Mobile application

\* Secure authentication

\* Cloud deployment

\* Model monitoring and drift detection

\* Privacy-preserving feature engineering



\---



\# 🎯 Vision



TrustBridge aims to explore a simple idea:



> \*\*A lack of traditional credit history should not automatically mean a lack of financial trust.\*\*



By combining alternative signals with explainable machine learning, TrustBridge explores how technology could help create more inclusive financial assessment systems.



\---



\# 👨‍💻 Author



\*\*Garv Bharadwaj\*\*



Built as an AI/ML project exploring:



\* Machine Learning

\* Alternative Credit Scoring

\* Explainable AI

\* Financial Technology

\* FastAPI

\* Full-Stack Development



\---



\## ⭐ If you find this project interesting



Give the repository a ⭐ and feel free to explore, improve, and contribute.




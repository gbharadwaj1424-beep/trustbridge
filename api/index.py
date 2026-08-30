"""
TrustBridge API
----------------
Serves the alt-data trust score model with per-feature explainability
and a plain-language explanation, plus preset demo personas so judges
can see a live result in seconds without typing data.

Run:  uvicorn app:app --reload --port 8000
"""
import json
import os
from typing import Dict

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="TrustBridge API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load(os.path.join(BASE_DIR, "model.joblib"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.joblib"))
with open(os.path.join(BASE_DIR, "feature_meta.json")) as fh:
    META = json.load(fh)

FEATURE_ORDER = [f["name"] for f in META["features"]]
FEATURE_LABELS = {f["name"]: f["label"] for f in META["features"]}


class SignalInput(BaseModel):
    upi_txn_frequency: float = Field(..., ge=0, le=100)
    upi_txn_regularity: float = Field(..., ge=0, le=100)
    avg_monthly_inflow: float = Field(..., ge=0, le=200000)
    recharge_regularity: float = Field(..., ge=0, le=100)
    utility_payment_timeliness: float = Field(..., ge=0, le=100)
    savings_growth_6m: float = Field(..., ge=-100, le=200)
    peer_vouches: float = Field(..., ge=0, le=5)
    business_vintage_months: float = Field(..., ge=0, le=600)
    geo_stability: float = Field(..., ge=0, le=100)
    digital_footprint_diversity: float = Field(..., ge=0, le=100)
    name: str = "Applicant"


PERSONAS: Dict[str, SignalInput] = {
    "vendor": SignalInput(
        name="Radha — Vegetable Cart Vendor",
        upi_txn_frequency=24, upi_txn_regularity=72,
        avg_monthly_inflow=16000, recharge_regularity=68,
        utility_payment_timeliness=80, savings_growth_6m=12,
        peer_vouches=3, business_vintage_months=48,
        geo_stability=85, digital_footprint_diversity=55,
    ),
    "gig_worker": SignalInput(
        name="Aman — Food Delivery Rider",
        upi_txn_frequency=35, upi_txn_regularity=58,
        avg_monthly_inflow=19000, recharge_regularity=75,
        utility_payment_timeliness=60, savings_growth_6m=-5,
        peer_vouches=1, business_vintage_months=14,
        geo_stability=40, digital_footprint_diversity=70,
    ),
    "farmer": SignalInput(
        name="Suresh — Smallholder Farmer",
        upi_txn_frequency=8, upi_txn_regularity=40,
        avg_monthly_inflow=9000, recharge_regularity=45,
        utility_payment_timeliness=55, savings_growth_6m=20,
        peer_vouches=4, business_vintage_months=120,
        geo_stability=95, digital_footprint_diversity=25,
    ),
    "risky_applicant": SignalInput(
        name="New Applicant — Thin Signal History",
        upi_txn_frequency=5, upi_txn_regularity=20,
        avg_monthly_inflow=6000, recharge_regularity=15,
        utility_payment_timeliness=30, savings_growth_6m=-20,
        peer_vouches=0, business_vintage_months=2,
        geo_stability=30, digital_footprint_diversity=15,
    ),
}


def _tier(score: float):
    if score >= 72:
        return "High Trust", "Eligible for standard micro-loan limits"
    if score >= 48:
        return "Building Trust", "Eligible for a small starter loan or savings-linked credit"
    return "Emerging", "Recommend starting with a savings product or group-guaranteed micro-loan"


def _recommend_product(score: float, features: Dict[str, float]):
    tier, base_action = _tier(score)
    if score >= 72:
        amount = "₹15,000 – ₹40,000"
        product = "Individual micro-loan"
    elif score >= 48:
        amount = "₹3,000 – ₹12,000"
        product = "Starter micro-loan / BNPL for inventory"
    else:
        amount = "₹500 – ₹2,000 (savings-linked)"
        product = "Group-guaranteed micro-loan or recurring digital savings plan"
    return {"tier": tier, "product": product, "suggested_amount": amount, "action": base_action}


def _explain(score: float, contributions: list, persona_name: str):
    tier, _ = _tier(score)
    top_positive = [c for c in contributions if c["impact"] > 0][:3]
    top_negative = [c for c in contributions if c["impact"] < 0][:2]

    parts = [f"{persona_name} received a trust score of {score:.0f}/100 ({tier})."]
    if top_positive:
        drivers = ", ".join(c["label"].lower() for c in top_positive)
        parts.append(f"This is mainly supported by strong {drivers}.")
    if top_negative:
        weak = ", ".join(c["label"].lower() for c in top_negative)
        parts.append(f"The main areas holding the score back are {weak}.")
    parts.append(
        "No formal bank statement or credit bureau record was used — "
        "this score is built entirely from everyday digital and community signals."
    )
    return " ".join(parts)


def score_signals(signals: SignalInput):
    x = np.array([[getattr(signals, f) for f in FEATURE_ORDER]])
    x_scaled = scaler.transform(x)

    prob = model.predict_proba(x_scaled)[0][1]
    score = round(float(prob) * 100, 1)

    coefs = META["coefficients"]
    contributions = []
    for i, fname in enumerate(FEATURE_ORDER):
        contribution = float(coefs[fname]) * float(x_scaled[0][i])
        contributions.append({
            "feature": fname,
            "label": FEATURE_LABELS[fname],
            "raw_value": getattr(signals, fname),
            "impact": round(contribution, 3),
        })
    contributions.sort(key=lambda c: abs(c["impact"]), reverse=True)

    recommendation = _recommend_product(score, {c["feature"]: c["raw_value"] for c in contributions})
    explanation = _explain(score, contributions, signals.name)

    return {
        "name": signals.name,
        "score": score,
        "tier": recommendation["tier"],
        "recommendation": recommendation,
        "contributions": contributions,
        "explanation": explanation,
    }


@app.get("/")
def root():
    return {"status": "ok", "service": "TrustBridge API"}


@app.get("/personas")
def list_personas():
    return {key: p.dict() for key, p in PERSONAS.items()}


@app.get("/score/persona/{persona_key}")
def score_persona(persona_key: str):
    if persona_key not in PERSONAS:
        raise HTTPException(status_code=404, detail="Unknown persona")
    return score_signals(PERSONAS[persona_key])


@app.post("/score")
def score_custom(signals: SignalInput):
    return score_signals(signals)


@app.get("/model-info")
def model_info():
    return {
        "val_auc": META["val_auc"],
        "val_accuracy": META["val_accuracy"],
        "features": META["features"],
        "note": "Trained on a synthetic dataset calibrated to published alt-data "
                "credit-signal literature. Swap in real, consented transaction data "
                "via the same feature schema for production use.",
    }

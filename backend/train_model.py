"""
TrustBridge — Trust Scoring for the Credit-Invisible
------------------------------------------------------
Generates a synthetic dataset of alternative (non-bank-statement) signals
for informal-economy earners (vendors, gig workers, farmers) and trains a
logistic regression model to predict a proxy "repayment reliability" label.

Why synthetic data?
Real alt-data (UPI logs, recharge history, utility bills) for the
credit-invisible is not publicly available at individual level due to
privacy. We simulate feature distributions and correlations informed by
published microfinance / alt-data credit-scoring literature (e.g. mobile
airtime top-up regularity and utility bill payment timeliness correlating
with loan repayment in studies from CGAP, IFC, and mobile-money lenders).
This lets us demonstrate a working, explainable scoring pipeline end to
end. In production this model would be retrained on real, consented data.

Run: python train_model.py
Produces: model.joblib, scaler.joblib, feature_meta.json
"""
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
import joblib

np.random.seed(42)
N = 6000

# ---- Feature definitions -------------------------------------------------
# Each tuple: (name, human_label, direction, description)
FEATURES = [
    ("upi_txn_frequency", "Digital transaction frequency (per month)", "+",
     "How often the person transacts digitally (UPI/wallet) per month."),
    ("upi_txn_regularity", "Transaction regularity score (0-100)", "+",
     "How consistent transaction timing/amounts are, month to month."),
    ("avg_monthly_inflow", "Average monthly digital inflow (INR)", "+",
     "Average money received digitally per month (proxy for earnings)."),
    ("recharge_regularity", "Mobile recharge regularity (0-100)", "+",
     "Consistency of prepaid mobile recharges — a known proxy for stable routine."),
    ("utility_payment_timeliness", "Utility bill payment timeliness (%)", "+",
     "Percent of electricity/water/gas bills paid on or before due date."),
    ("savings_growth_6m", "Savings/wallet balance growth over 6 months (%)", "+",
     "Trend in digital wallet or savings balance over the last 6 months."),
    ("peer_vouches", "Verified peer/community vouches (0-5)", "+",
     "Number of verified vouches from community members or trade association."),
    ("business_vintage_months", "Business/work vintage (months)", "+",
     "How long the person has been doing this work or running this business."),
    ("geo_stability", "Location stability score (0-100)", "+",
     "How stable the person's operating location / service area is over time."),
    ("digital_footprint_diversity", "Digital footprint diversity (0-100)", "+",
     "Diversity of everyday app usage (marketplace, delivery, payments, etc.)."),
]

FEATURE_NAMES = [f[0] for f in FEATURES]


def generate_dataset(n=N):
    data = {}
    data["upi_txn_frequency"] = np.clip(np.random.normal(18, 8, n), 0, 60)
    data["upi_txn_regularity"] = np.clip(np.random.normal(55, 20, n), 0, 100)
    data["avg_monthly_inflow"] = np.clip(np.random.normal(14000, 7000, n), 1000, 60000)
    data["recharge_regularity"] = np.clip(np.random.normal(50, 22, n), 0, 100)
    data["utility_payment_timeliness"] = np.clip(np.random.normal(65, 20, n), 0, 100)
    data["savings_growth_6m"] = np.clip(np.random.normal(4, 15, n), -50, 80)
    data["peer_vouches"] = np.clip(np.random.poisson(1.6, n), 0, 5)
    data["business_vintage_months"] = np.clip(np.random.exponential(24, n), 0, 240)
    data["geo_stability"] = np.clip(np.random.normal(60, 22, n), 0, 100)
    data["digital_footprint_diversity"] = np.clip(np.random.normal(50, 20, n), 0, 100)

    df = pd.DataFrame(data)

    # Latent "reliability" combines features with weights reflecting
    # plausible real-world importance, plus noise, then thresholded.
    z = (
        0.9 * (df["upi_txn_regularity"] - 50) / 20
        + 0.8 * (df["utility_payment_timeliness"] - 60) / 20
        + 0.7 * (df["recharge_regularity"] - 50) / 20
        + 0.6 * (df["peer_vouches"] - 1.5) / 1.2
        + 0.5 * (df["savings_growth_6m"]) / 15
        + 0.4 * (df["geo_stability"] - 55) / 20
        + 0.35 * np.log1p(df["business_vintage_months"]) / 2
        + 0.3 * (df["digital_footprint_diversity"] - 50) / 20
        + 0.25 * (df["upi_txn_frequency"] - 18) / 8
        + 0.2 * (np.log1p(df["avg_monthly_inflow"]) - 9.2) / 0.6
        + np.random.normal(0, 1.0, n)  # noise / unexplained variance
    )
    prob = 1 / (1 + np.exp(-z))
    df["repaid_reliably"] = (np.random.uniform(0, 1, n) < prob).astype(int)
    return df


def main():
    df = generate_dataset()
    X = df[FEATURE_NAMES].values
    y = df["repaid_reliably"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_s, y_train)

    auc = roc_auc_score(y_test, model.predict_proba(X_test_s)[:, 1])
    acc = accuracy_score(y_test, model.predict(X_test_s))
    print(f"Validation AUC: {auc:.3f} | Accuracy: {acc:.3f}")

    joblib.dump(model, "model.joblib")
    joblib.dump(scaler, "scaler.joblib")

    meta = {
        "features": [
            {"name": f[0], "label": f[1], "direction": f[2], "description": f[3]}
            for f in FEATURES
        ],
        "coefficients": dict(zip(FEATURE_NAMES, model.coef_[0].tolist())),
        "intercept": float(model.intercept_[0]),
        "val_auc": auc,
        "val_accuracy": acc,
    }
    with open("feature_meta.json", "w") as fh:
        json.dump(meta, fh, indent=2)

    print("Saved model.joblib, scaler.joblib, feature_meta.json")


if __name__ == "__main__":
    main()

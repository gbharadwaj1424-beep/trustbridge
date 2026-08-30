import { useEffect, useState } from "react";
import axios from "axios";
import ScoreGauge from "../components/ScoreGauge";
import ContributionChart from "../components/ContributionChart";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const FIELD_META = [
  { key: "upi_txn_frequency", label: "Digital txns / month", max: 60 },
  { key: "upi_txn_regularity", label: "Transaction regularity (0-100)", max: 100 },
  { key: "avg_monthly_inflow", label: "Avg. monthly inflow (₹)", max: 60000 },
  { key: "recharge_regularity", label: "Recharge regularity (0-100)", max: 100 },
  { key: "utility_payment_timeliness", label: "Utility bill timeliness (%)", max: 100 },
  { key: "savings_growth_6m", label: "Savings growth, 6mo (%)", max: 80, min: -50 },
  { key: "peer_vouches", label: "Peer/community vouches", max: 5 },
  { key: "business_vintage_months", label: "Business vintage (months)", max: 240 },
  { key: "geo_stability", label: "Location stability (0-100)", max: 100 },
  { key: "digital_footprint_diversity", label: "Digital footprint diversity (0-100)", max: 100 },
];

const PERSONA_LABELS = {
  vendor: "🥬 Vendor",
  gig_worker: "🛵 Gig worker",
  farmer: "🌾 Farmer",
  risky_applicant: "🆕 Thin-file applicant",
};

export default function Home() {
  const [personas, setPersonas] = useState({});
  const [activePersona, setActivePersona] = useState("vendor");
  const [signals, setSignals] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [modelInfo, setModelInfo] = useState(null);

  useEffect(() => {
    axios.get(`${API_URL}/personas`).then((res) => setPersonas(res.data)).catch(() => {});
    axios.get(`${API_URL}/model-info`).then((res) => setModelInfo(res.data)).catch(() => {});
  }, []);

  useEffect(() => {
    if (personas[activePersona]) {
      setSignals(personas[activePersona]);
    }
  }, [personas, activePersona]);

  const runScore = async (payload) => {
    setLoading(true);
    setError("");
    try {
      const res = await axios.post(`${API_URL}/score`, payload);
      setResult(res.data);
    } catch (e) {
      setError("Couldn't reach the scoring API. Is the backend running on :8000?");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (signals) runScore(signals);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activePersona, personas]);

  const handleFieldChange = (key, value) => {
    setSignals((prev) => ({ ...prev, [key]: parseFloat(value) }));
  };

  return (
    <div className="min-h-screen bg-sand">
      <header className="bg-teal text-white py-8 px-6 md:px-16">
        <div className="max-w-6xl mx-auto flex items-center justify-between flex-wrap gap-3">
          <div>
            <h1 className="text-3xl font-bold">TrustBridge</h1>
            <p className="text-white/80 mt-1 text-sm md:text-base">
              Trust scoring for the credit-invisible — no bank statement required.
            </p>
          </div>
          {modelInfo && (
            <div className="text-right text-sm text-white/80">
              <div>Model validation AUC: <span className="font-semibold text-white">{modelInfo.val_auc.toFixed(2)}</span></div>
              <div>Trained on synthetic alt-data signals</div>
            </div>
          )}
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 md:px-16 py-10 grid gap-8 lg:grid-cols-[340px_1fr]">
        {/* Left: input panel */}
        <section className="bg-white rounded-2xl shadow-sm p-6 h-fit">
          <h2 className="font-semibold text-ink mb-3">Choose a demo applicant</h2>
          <div className="grid grid-cols-2 gap-2 mb-6">
            {Object.keys(PERSONA_LABELS).map((key) => (
              <button
                key={key}
                onClick={() => setActivePersona(key)}
                className={`text-sm py-2 px-3 rounded-lg border transition ${
                  activePersona === key
                    ? "bg-teal text-white border-teal"
                    : "bg-white text-ink border-ink/15 hover:border-teal"
                }`}
              >
                {PERSONA_LABELS[key]}
              </button>
            ))}
          </div>

          <h2 className="font-semibold text-ink mb-3">Or adjust signals manually</h2>
          <div className="space-y-3 max-h-[420px] overflow-y-auto pr-1">
            {signals &&
              FIELD_META.map((f) => (
                <div key={f.key}>
                  <div className="flex justify-between text-xs text-ink/70 mb-1">
                    <span>{f.label}</span>
                    <span className="font-medium">{signals[f.key]}</span>
                  </div>
                  <input
                    type="range"
                    min={f.min ?? 0}
                    max={f.max}
                    value={signals[f.key]}
                    onChange={(e) => handleFieldChange(f.key, e.target.value)}
                    className="w-full accent-teal"
                  />
                </div>
              ))}
          </div>

          <button
            onClick={() => signals && runScore(signals)}
            disabled={loading}
            className="mt-5 w-full bg-mint hover:bg-seafoam transition text-white font-semibold py-2.5 rounded-lg disabled:opacity-60"
          >
            {loading ? "Scoring…" : "Recalculate score"}
          </button>
          {error && <p className="text-sm text-red-600 mt-3">{error}</p>}
        </section>

        {/* Right: results */}
        <section className="space-y-6">
          {result && (
            <>
              <div className="bg-white rounded-2xl shadow-sm p-6 grid md:grid-cols-[220px_1fr] gap-6 items-center">
                <ScoreGauge score={result.score} tier={result.tier} />
                <div>
                  <h3 className="text-xl font-bold text-ink mb-1">{result.name}</h3>
                  <p className="text-ink/70 text-sm leading-relaxed mb-4">{result.explanation}</p>
                  <div className="bg-sand rounded-xl p-4 border border-ink/10">
                    <p className="text-xs uppercase tracking-wide text-ink/50 mb-1">Recommended product</p>
                    <p className="font-semibold text-ink">{result.recommendation.product}</p>
                    <p className="text-sm text-ink/70">{result.recommendation.suggested_amount} &middot; {result.recommendation.action}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-2xl shadow-sm p-6">
                <h3 className="font-semibold text-ink mb-1">What's driving this score</h3>
                <p className="text-xs text-ink/50 mb-4">Green = pushes trust up · Red = pulls trust down</p>
                <ContributionChart contributions={result.contributions} />
              </div>
            </>
          )}
        </section>
      </main>

      <footer className="text-center text-xs text-ink/40 pb-8">
        Built for Build Bank Hackathon · IIT Delhi — Track 1: Financial Inclusion
      </footer>
    </div>
  );
}

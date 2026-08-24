import { useState } from "react";
import { checkPCOS } from "../services/api";
import { Card, ErrorBanner } from "../components/Feedback";

const YES_NO_FIELDS = [
  ["weight_gain", "Recent weight gain"],
  ["hair_growth", "Excess hair growth"],
  ["skin_darkening", "Skin darkening"],
  ["hair_loss", "Hair loss"],
  ["pimples", "Frequent pimples"],
  ["fast_food", "Frequent fast food intake"],
  ["exercise", "Regular exercise"],
];

const INITIAL = {
  age: "",
  weight: "",
  height: "",
  cycle: "",
  cycle_length: "",
  weight_gain: 0,
  hair_growth: 0,
  skin_darkening: 0,
  hair_loss: 0,
  pimples: 0,
  fast_food: 0,
  exercise: 0,
};

export default function PCOSChecker() {
  const [form, setForm] = useState(INITIAL);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);

    const payload = {
      age: Number(form.age),
      weight: Number(form.weight),
      height: Number(form.height),
      cycle: Number(form.cycle),
      cycle_length: Number(form.cycle_length),
      weight_gain: Number(form.weight_gain),
      hair_growth: Number(form.hair_growth),
      skin_darkening: Number(form.skin_darkening),
      hair_loss: Number(form.hair_loss),
      pimples: Number(form.pimples),
      fast_food: Number(form.fast_food),
      exercise: Number(form.exercise),
    };

    try {
      const data = await checkPCOS(payload);
      setResult(data);
    } catch (err) {
      setError(err?.message || "Could not run the PCOS check.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1>PCOS Checker</h1>
        <p className="page-subtitle">
          An informational ML screening tool — this is not a medical diagnosis.
        </p>
      </header>

      <section className="grid grid-2-uneven">
        <Card title="Enter your details">
          <form onSubmit={handleSubmit} className="form">
            <ErrorBanner message={error} />

            <div className="field-row">
              <label className="field">
                <span>Age</span>
                <input type="number" required min="0" value={form.age}
                  onChange={(e) => updateField("age", e.target.value)} />
              </label>
              <label className="field">
                <span>Weight (kg)</span>
                <input type="number" required min="0" step="0.1" value={form.weight}
                  onChange={(e) => updateField("weight", e.target.value)} />
              </label>
            </div>

            <div className="field-row">
              <label className="field">
                <span>Height (cm)</span>
                <input type="number" required min="0" step="0.1" value={form.height}
                  onChange={(e) => updateField("height", e.target.value)} />
              </label>
              <label className="field">
                <span>Cycle (R/I)</span>
                <select required value={form.cycle} onChange={(e) => updateField("cycle", e.target.value)}>
                  <option value="">Select</option>
                  <option value="2">Regular</option>    {/* cv */}
                  <option value="4">Irregular</option>
                </select>
              </label>
            </div>

            <label className="field">
              <span>Average cycle length (days)</span>
              <input type="number" required min="0" step="0.1" value={form.cycle_length}
                onChange={(e) => updateField("cycle_length", e.target.value)} />
            </label>

            {YES_NO_FIELDS.map(([field, label]) => (
              <label key={field} className="field field-inline">
                <span>{label}</span>
                <select
                  value={form[field]}
                  onChange={(e) => updateField(field, e.target.value)}
                >
                  <option value={0}>No</option>
                  <option value={1}>Yes</option>
                </select>
              </label>
            ))}

            <button className="btn btn-primary btn-block" type="submit" disabled={loading}>
              {loading ? "Checking..." : "Check PCOS risk"}
            </button>
          </form>
        </Card>

        <Card title="Result">
          {!result ? (
            <p className="muted">Fill in the form and submit to see your result here.</p>
          ) : (
            <div className="result-block">
              <div className="result-row">
                <span>Prediction</span>
                <strong>{result.prediction}</strong>
              </div>
              <div className="result-row">
                <span>Value</span>
                <strong>{result.value}</strong>
              </div>
              <div className="result-row">
                <span>Confidence</span>
                <strong>{typeof result.confidence === "number" ? `${result.confidence.toFixed(1)}%` : result.confidence}</strong> {/* cv */}
              </div>
              <p className="disclaimer">
                This is an informational ML screening result, not a medical diagnosis. Please consult a
                qualified doctor for proper evaluation.
              </p>
            </div>
          )}
        </Card>
      </section>
    </div>
  );
}

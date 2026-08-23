import { useState } from "react";
import { trackCycle } from "../services/api";
import { Card, ErrorBanner } from "../components/Feedback";

export default function CycleTracker() {
  const [form, setForm] = useState({
    last_period: new Date().toISOString().slice(0, 10),
    cycle_length: 28,
    period_duration: 5,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const data = await trackCycle({
        last_period: form.last_period,
        cycle_length: Number(form.cycle_length),
        period_duration: Number(form.period_duration),
      });
      setResult(data.result);
    } catch (err) {
      setError(err?.message || "Could not analyze cycle.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1>Cycle Tracker</h1>
        <p className="page-subtitle">Estimate your current cycle phase and next period.</p>
      </header>

      <section className="grid grid-2-uneven">
        <Card title="Enter cycle details">
          <form onSubmit={handleSubmit} className="form">
            <ErrorBanner message={error} />

            <label className="field">
              <span>Last period start date</span>
              <input
                type="date"
                required
                value={form.last_period}
                onChange={(e) => updateField("last_period", e.target.value)}
              />
            </label>

            <div className="field-row">
              <label className="field">
                <span>Cycle length (days)</span>
                <input
                  type="number"
                  required
                  min="1"
                  value={form.cycle_length}
                  onChange={(e) => updateField("cycle_length", e.target.value)}
                />
              </label>

              <label className="field">
                <span>Period duration (days)</span>
                <input
                  type="number"
                  required
                  min="1"
                  value={form.period_duration}
                  onChange={(e) => updateField("period_duration", e.target.value)}
                />
              </label>
            </div>

            <button className="btn btn-primary btn-block" type="submit" disabled={loading}>
              {loading ? "Analyzing..." : "Analyze cycle"}
            </button>
          </form>
        </Card>

        <Card title="Result">
          {!result ? (
            <p className="muted">Fill in the form and submit to see your result here.</p>
          ) : (
            <pre className="result-text">{result}</pre>
          )}
        </Card>
      </section>
    </div>
  );
}

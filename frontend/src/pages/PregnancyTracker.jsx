import { useState } from "react";
import { trackPregnancy } from "../services/api";
import { Card, ErrorBanner } from "../components/Feedback";

export default function PregnancyTracker() {
  const [lmpDate, setLmpDate] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!lmpDate) return;
    setError(null);
    setLoading(true);
    try {
      const data = await trackPregnancy(lmpDate);
      setResult(data.result);
    } catch (err) {
      setError(err?.message || "Could not calculate pregnancy details.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1>Pregnancy Tracker</h1>
        <p className="page-subtitle">Enter your last menstrual period (LMP) date to see your journey.</p>
      </header>

      <section className="grid grid-2-uneven">
        <Card title="Enter your LMP date">
          <form onSubmit={handleSubmit} className="form">
            <ErrorBanner message={error} />

            <label className="field">
              <span>Last menstrual period date</span>
              <input
                type="date"
                required
                value={lmpDate}
                onChange={(e) => setLmpDate(e.target.value)}
              />
            </label>

            <button className="btn btn-primary btn-block" type="submit" disabled={loading}>
              {loading ? "Calculating..." : "Track pregnancy"}
            </button>
          </form>
        </Card>

        <Card title="Result">
          {!result ? (
            <p className="muted">Enter your LMP date and submit to see your result here.</p>
          ) : (
            <pre className="result-text">{result}</pre>
          )}
        </Card>
      </section>
    </div>
  );
}

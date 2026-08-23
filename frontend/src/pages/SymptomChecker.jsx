import { useState } from "react";
import { checkSymptoms } from "../services/api";
import { Card, EmptyState, ErrorBanner } from "../components/Feedback";

export default function SymptomChecker() {
  const [symptoms, setSymptoms] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!symptoms.trim()) return;
    setError(null);
    setLoading(true);
    try {
      const data = await checkSymptoms(symptoms.trim());
      setResults(data.results || []);
    } catch (err) {
      setError(err?.message || "Could not check symptoms.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1>Symptom Checker</h1>
        <p className="page-subtitle">
          Describe your symptoms to see possible matches. This is not a medical diagnosis.
        </p>
      </header>

      <Card title="Describe your symptoms">
        <form onSubmit={handleSubmit} className="form form-inline">
          <ErrorBanner message={error} />
          <textarea
            rows={3}
            placeholder="e.g. heavy bleeding, fatigue, cramps..."
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
          />
          <button className="btn btn-primary" type="submit" disabled={loading || !symptoms.trim()}>
            {loading ? "Checking..." : "Check symptoms"}
          </button>
        </form>
      </Card>

      {results && (
        <Card title="Possible Matches">
          {results.length === 0 ? (
            <EmptyState message="No confident matches found. Consider consulting a doctor or using the AI chat for more guidance." />
          ) : (
            <div className="pattern-list">
              {results.map((condition, idx) => (
                <div key={idx} className="pattern-item">
                  <div className="pattern-header">
                    <span className="pattern-title">{condition.name}</span>
                    <span className="pattern-severity">Score: {condition.score}</span>
                  </div>
                  <p className="pattern-message">
                    <strong>Category:</strong> {condition.category}
                  </p>
                  <p className="pattern-message">{condition.description}</p>
                  {condition.matched && condition.matched.length > 0 && (
                    <ul className="pattern-evidence">
                      {condition.matched.map((m, i) => (
                        <li key={i}>{m}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
              <p className="disclaimer">
                These are possible matches only, not a confirmed diagnosis. Please consult a qualified
                gynecologist for proper evaluation.
              </p>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}

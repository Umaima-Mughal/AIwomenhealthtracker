import { useMemo, useState } from "react";   //cv
import { trackPregnancy } from "../services/api";
import { Card, ErrorBanner } from "../components/Feedback";

function parsePregnancyResult(rawResult) {
  if (!rawResult) return null;

  const lines = rawResult
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  const getValueAfter = (label) => {
    const index = lines.findIndex((line) => line.replace(":", "") === label);
    return index >= 0 ? lines[index + 1] : null;
  };

  const recommendationsIndex = lines.findIndex((line) => line.replace(":", "") === "Recommendations");
  const noteIndex = lines.findIndex((line) => line.replace(":", "") === "Note");

  return {
    currentWeek: getValueAfter("Current Week"),
    daysPregnant: getValueAfter("Days Pregnant"),
    trimester: getValueAfter("Trimester"),
    dueDate: getValueAfter("Expected Due Date"),
    babySize: getValueAfter("Baby Size"),
    babyDevelopment: getValueAfter("Baby Development"),
    maternalChanges: getValueAfter("Maternal Changes"),
    recommendations:
      recommendationsIndex >= 0
        ? lines
            .slice(recommendationsIndex + 1, noteIndex >= 0 ? noteIndex : undefined)
            .filter((line) => !line.endsWith(":"))
        : [],
    note: noteIndex >= 0 ? lines.slice(noteIndex + 1).join(" ") : null,
  };
}

export default function PregnancyTracker() {
  const [lmpDate, setLmpDate] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const parsedResult = useMemo(() => parsePregnancyResult(result), [result]);

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
          {!parsedResult ? (
            <p className="muted">Enter your LMP date and submit to see your result here.</p>
          ) : (
            <div className="result-block">
              <div className="result-row">
                <span>Current week</span>
                <strong>{parsedResult.currentWeek || "N/A"}</strong>
              </div>
              <div className="result-row">
                <span>Days pregnant</span>
                <strong>{parsedResult.daysPregnant || "N/A"}</strong>
              </div>
              <div className="result-row">
                <span>Trimester</span>
                <strong>{parsedResult.trimester || "N/A"}</strong>
              </div>
              <div className="result-row">
                <span>Expected due date</span>
                <strong>{parsedResult.dueDate || "N/A"}</strong>
              </div>

              {parsedResult.babySize && (
                <section className="pattern-item">
                  <div className="pattern-header">
                    <span className="pattern-title">Baby size</span>
                  </div>
                  <p className="pattern-message">{parsedResult.babySize}</p>
                </section>
              )}

              {parsedResult.babyDevelopment && (
                <section className="pattern-item">
                  <div className="pattern-header">
                    <span className="pattern-title">Baby development</span>
                  </div>
                  <p className="pattern-message">{parsedResult.babyDevelopment}</p>
                </section>
              )}

              {parsedResult.maternalChanges && (
                <section className="pattern-item">
                  <div className="pattern-header">
                    <span className="pattern-title">Maternal changes</span>
                  </div>
                  <p className="pattern-message">{parsedResult.maternalChanges}</p>
                </section>
              )}

              {parsedResult.recommendations.length > 0 && (
                <section className="pattern-item">
                  <div className="pattern-header">
                    <span className="pattern-title">Recommendations</span>
                  </div>
                  <ul className="pattern-evidence">
                    {parsedResult.recommendations.map((recommendation, index) => (
                      <li key={index}>{recommendation}</li>
                    ))}
                  </ul>
                </section>
              )}

              <p className="disclaimer">
                {parsedResult.note || "This tracker provides health information only and is not a medical diagnosis."}
              </p>
            </div>
          )}
        </Card>
      </section>
    </div>
  );
}
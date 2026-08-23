import { useEffect } from "react";
import { getDoctorSummary } from "../services/api";
import { useApi } from "../hooks/useApi";
import { Card, Spinner, EmptyState, ErrorBanner } from "../components/Feedback";

export default function DoctorSummary() {
  const { data, loading, error, run } = useApi(getDoctorSummary);

  useEffect(() => {
    run();
  }, [run]);

  return (
    <div className="page">
      <header className="page-header">
        <h1>Doctor Summary</h1>
        <p className="page-subtitle">
          A shareable summary of detected health patterns, generated from your tracked data. Not a medical
          diagnosis.
        </p>
      </header>

      <ErrorBanner message={error} />

      {loading ? (
        <Spinner label="Generating summary..." />
      ) : !data ? null : (
        <>
          <section className="grid grid-3">
            <Card title="Summary Period">
              <div className="stat stat-text">
                {data.period?.from} – {data.period?.to}
              </div>
            </Card>
            <Card title="Overall Status">
              <div className="stat stat-text">{data.overall_status || "N/A"}</div>
            </Card>
            <Card title="Patterns Detected">
              <div className="stat">{data.pattern_count ?? 0}</div>
            </Card>
          </section>

          <Card title="Detected Patterns" className="doctor-patterns">
            {!data.patterns_detected || data.patterns_detected.length === 0 ? (
              <EmptyState message="No notable patterns detected in the last 3 months." />
            ) : (
              <div className="pattern-list">
                {data.patterns_detected.map((pattern, idx) => (
                  <div key={idx} className={`pattern-item severity-${pattern.severity || "info"}`}>
                    <div className="pattern-header">
                      <span className="pattern-title">{pattern.title}</span>
                      <span className="pattern-severity">{pattern.severity}</span>
                    </div>
                    <p className="pattern-message">{pattern.message}</p>
                    {pattern.evidence && pattern.evidence.length > 0 && (
                      <ul className="pattern-evidence">
                        {pattern.evidence.map((ev, i) => (
                          <li key={i}>{typeof ev === "string" ? ev : JSON.stringify(ev)}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}
              </div>
            )}
          </Card>
        </>
      )}
    </div>
  );
}

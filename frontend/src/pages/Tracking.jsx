import { useEffect, useState } from "react";
import { getTrackingHistory, createTracking } from "../services/api";
import { useApi } from "../hooks/useApi";
import { Card, Spinner, EmptyState, ErrorBanner, SuccessBanner } from "../components/Feedback";

const EMPTY_FORM = {
  date: new Date().toISOString().slice(0, 10),
  symptoms: "",
  mood: "",
  sleep_hours: "",
  weight: "",
  cycle_day: "",
  period_started: "",
  notes: "",
};

export default function Tracking() {
  const { data: entries, loading, error, run } = useApi(getTrackingHistory);
  const [form, setForm] = useState(EMPTY_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    run();
  }, [run]);

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitError(null);
    setSuccess(false);
    setSubmitting(true);

    const payload = {
      date: form.date,
      symptoms: form.symptoms || null,
      mood: form.mood || null,
      sleep_hours: form.sleep_hours === "" ? null : Number(form.sleep_hours),
      weight: form.weight === "" ? null : Number(form.weight),
      cycle_day: form.cycle_day === "" ? null : Number(form.cycle_day),
      period_started: form.period_started || null,
      notes: form.notes || null,
    };

    try {
      await createTracking(payload);
      setSuccess(true);
      setForm(EMPTY_FORM);
      await run(); // refresh history so the new entry shows up
    } catch (err) {
      setSubmitError(err?.message || "Could not save this entry.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1>Tracking</h1>
        <p className="page-subtitle">Log daily health data and review your history.</p>
      </header>

      <section className="grid grid-2-uneven">
        <Card title="New Entry">
          <form onSubmit={handleSubmit} className="form">
            <ErrorBanner message={submitError} />
            <SuccessBanner message={success ? "Entry saved." : null} />

            <label className="field">
              <span>Date</span>
              <input
                type="date"
                required
                value={form.date}
                onChange={(e) => updateField("date", e.target.value)}
              />
            </label>

            <label className="field">
              <span>Mood</span>
              <input
                type="text"
                placeholder="e.g. Calm, Anxious, Happy"
                value={form.mood}
                onChange={(e) => updateField("mood", e.target.value)}
              />
            </label>

            <div className="field-row">
              <label className="field">
                <span>Sleep hours</span>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  value={form.sleep_hours}
                  onChange={(e) => updateField("sleep_hours", e.target.value)}
                />
              </label>

              <label className="field">
                <span>Weight</span>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  value={form.weight}
                  onChange={(e) => updateField("weight", e.target.value)}
                />
              </label>
            </div>

            <div className="field-row">
              <label className="field">
                <span>Cycle day</span>
                <input
                  type="number"
                  min="0"
                  value={form.cycle_day}
                  onChange={(e) => updateField("cycle_day", e.target.value)}
                />
              </label>

              <label className="field">
                <span>Period started?</span>
                <select
                  value={form.period_started}
                  onChange={(e) => updateField("period_started", e.target.value)}
                >
                  <option value="">Not specified</option>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </label>
            </div>

            <label className="field">
              <span>Symptoms</span>
              <input
                type="text"
                placeholder="e.g. Cramps, headache"
                value={form.symptoms}
                onChange={(e) => updateField("symptoms", e.target.value)}
              />
            </label>

            <label className="field">
              <span>Notes</span>
              <textarea
                rows={3}
                value={form.notes}
                onChange={(e) => updateField("notes", e.target.value)}
              />
            </label>

            <button className="btn btn-primary btn-block" type="submit" disabled={submitting}>
              {submitting ? "Saving..." : "Save entry"}
            </button>
          </form>
        </Card>

        <Card title="Tracking History">
          <ErrorBanner message={error} />
          {loading ? (
            <Spinner label="Loading tracking history..." />
          ) : !entries || entries.length === 0 ? (
            <EmptyState message="No tracking entries yet. Add your first entry to see it here." />
          ) : (
            <ul className="entry-list">
              {entries.map((entry) => (
                <li key={entry.id} className="entry-list-item">
                  <div className="entry-list-date">{entry.date}</div>
                  <div className="entry-list-details">
                    {entry.mood && <span className="tag">Mood: {entry.mood}</span>}
                    {entry.sleep_hours != null && <span className="tag">Sleep: {entry.sleep_hours}h</span>}
                    {entry.weight != null && <span className="tag">Weight: {entry.weight}</span>}
                    {entry.cycle_day != null && <span className="tag">Cycle day: {entry.cycle_day}</span>}
                    {entry.period_started && <span className="tag">Period: {entry.period_started}</span>}
                    {entry.symptoms && <span className="tag">Symptoms: {entry.symptoms}</span>}
                  </div>
                  {entry.notes && <div className="entry-list-notes">{entry.notes}</div>}
                </li>
              ))}
            </ul>
          )}
        </Card>
      </section>
    </div>
  );
}

import { useEffect } from "react";
import { getThreeMonthHistory } from "../services/api";
import { useApi } from "../hooks/useApi";
import { Card, Spinner, EmptyState, ErrorBanner } from "../components/Feedback";

export default function History() {
  const { data, loading, error, run } = useApi(getThreeMonthHistory);

  useEffect(() => {
    run();
  }, [run]);

  return (
    <div className="page">
      <header className="page-header">
        <h1>3-Month Health History</h1>
        <p className="page-subtitle">
          {data?.period
            ? `${data.period.from} — ${data.period.to}`
            : "Tracking, chat, insights, and notifications from the last 90 days."}
        </p>
      </header>

      <ErrorBanner message={error} />

      {loading ? (
        <Spinner label="Loading history..." />
      ) : !data ? null : (
        <div className="grid grid-2">
          <Card title={`Tracking Records (${data.tracking?.length || 0})`}>
            {!data.tracking || data.tracking.length === 0 ? (
              <EmptyState message="No tracking records in the last 3 months." />
            ) : (
              <ul className="entry-list">
                {data.tracking.map((entry) => (
                  <li key={entry.id} className="entry-list-item">
                    <div className="entry-list-date">{entry.date}</div>
                    <div className="entry-list-details">
                      {entry.mood && <span className="tag">Mood: {entry.mood}</span>}
                      {entry.sleep_hours != null && <span className="tag">Sleep: {entry.sleep_hours}h</span>}
                      {entry.symptoms && <span className="tag">Symptoms: {entry.symptoms}</span>}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </Card>

          <Card title={`Chat Messages (${data.chat_messages?.length || 0})`}>
            {!data.chat_messages || data.chat_messages.length === 0 ? (
              <EmptyState message="No chat activity in the last 3 months." />
            ) : (
              <ul className="entry-list">
                {data.chat_messages.map((msg) => (
                  <li key={msg.id} className="entry-list-item">
                    <div className="entry-list-date">{msg.role}</div>
                    <div className="entry-list-notes">{msg.content}</div>
                  </li>
                ))}
              </ul>
            )}
          </Card>

          <Card title={`Insights (${data.insights?.length || 0})`}>
            {!data.insights || data.insights.length === 0 ? (
              <EmptyState message="No recorded insights yet." />
            ) : (
              <ul className="entry-list">
                {data.insights.map((insight) => (
                  <li key={insight.id} className="entry-list-item">
                    <div className="entry-list-date">{insight.title}</div>
                    <div className="entry-list-notes">{insight.description}</div>
                  </li>
                ))}
              </ul>
            )}
          </Card>

          <Card title={`Notifications (${data.notifications?.length || 0})`}>
            {!data.notifications || data.notifications.length === 0 ? (
              <EmptyState message="No notifications yet." />
            ) : (
              <ul className="entry-list">
                {data.notifications.map((note) => (
                  <li key={note.id} className="entry-list-item">
                    <div className="entry-list-date">{note.title}</div>
                    <div className="entry-list-notes">{note.message}</div>
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </div>
      )}
    </div>
  );
}

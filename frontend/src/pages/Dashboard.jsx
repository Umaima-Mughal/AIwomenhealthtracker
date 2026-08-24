import { useEffect } from "react";
import { Link } from "react-router-dom";
import {
  Activity,
  CalendarDays,
  HeartPulse,
  MessageCircle,
  Microscope,
  Stethoscope,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useApi } from "../hooks/useApi";
import { getTrackingHistory } from "../services/api";
import { Card, Spinner, EmptyState, ErrorBanner } from "../components/Feedback";

const QUICK_ACTIONS = [
  { to: "/tracking", label: "Log tracking entry", icon: Activity },
  { to: "/chat", label: "Ask the AI chat", icon: MessageCircle },
  { to: "/pcos-checker", label: "Run PCOS checker", icon: Microscope },
  { to: "/symptom-checker", label: "Check symptoms", icon: HeartPulse },
  { to: "/doctor-summary", label: "View doctor summary", icon: Stethoscope },
  { to: "/history", label: "View 3-month history", icon: CalendarDays },
];

export default function Dashboard() {
  const { user } = useAuth();
  const { data: entries, loading, error, run } = useApi(getTrackingHistory);

  useEffect(() => {
    run();
  }, [run]);

  const latest = entries && entries.length > 0 ? entries[0] : null;
  const recent = entries ? entries.slice(0, 5) : [];

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p className="page-subtitle">
            {user?.email ? `Welcome back, ${user.email}` : "Welcome back"}
          </p>
        </div>
      </header>

      <ErrorBanner message={error} />

      <section className="grid grid-3">
        <Card title="Current Cycle Day">
          {loading ? (
            <Spinner label="Loading..." />
          ) : latest?.cycle_day != null ? (
            <div className="stat">{latest.cycle_day}</div>
          ) : (
            <EmptyState message="No cycle data recorded yet." />
          )}
        </Card>

        <Card title="Latest Mood">
          {loading ? (
            <Spinner label="Loading..." />
          ) : latest?.mood ? (
            <div className="stat stat-text">{latest.mood}</div>
          ) : (
            <EmptyState message="No mood recorded yet." />
          )}
        </Card>

        <Card title="Latest Sleep">
          {loading ? (
            <Spinner label="Loading..." />
          ) : latest?.sleep_hours != null ? (
            <div className="stat">{latest.sleep_hours}h</div>
          ) : (
            <EmptyState message="No sleep data recorded yet." />
          )}
        </Card>
      </section>

      <section className="grid grid-2">
        <Card title="Recent Tracking Entries">
          {loading ? (
            <Spinner label="Loading tracking history..." />
          ) : recent.length === 0 ? (
            <EmptyState message="No tracking entries yet. Log your first entry to see it here." />
          ) : (
            <ul className="entry-list">
              {recent.map((entry) => (
                <li key={entry.id} className="entry-list-item">
                  <div className="entry-list-date">{entry.date}</div>
                  <div className="entry-list-details">
                    {entry.mood && <span className="tag">Mood: {entry.mood}</span>}
                    {entry.sleep_hours != null && <span className="tag">Sleep: {entry.sleep_hours}h</span>}
                    {entry.weight != null && <span className="tag">Weight: {entry.weight}</span>}
                    {entry.symptoms && <span className="tag">Symptoms: {entry.symptoms}</span>}
                  </div>
                </li>
              ))}
            </ul>
          )}
          <Link className="link-more" to="/tracking">
            View all tracking →
          </Link>
        </Card>

        <Card title="Quick Actions">
          <div className="quick-actions">
              {QUICK_ACTIONS.map((action) => {
              const Icon = action.icon;

              return (
                <Link key={action.to} to={action.to} className="quick-action">
                  <Icon className="quick-action-icon" aria-hidden="true" />
                  {action.label}
                </Link>
              );
            })}
          </div>
        </Card>
      </section>
    </div>
  );
}

import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../context/AuthContext";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: "🏠", end: true },
  { to: "/tracking", label: "Tracking", icon: "📈" },
  { to: "/chat", label: "AI Chat", icon: "💬" },
  { to: "/history", label: "3-Month History", icon: "🗓️" },
  { to: "/doctor-summary", label: "Doctor Summary", icon: "🩺" },
  { to: "/pcos-checker", label: "PCOS Checker", icon: "🔬" },
  { to: "/symptom-checker", label: "Symptom Checker", icon: "🩹" },
  { to: "/cycle-tracker", label: "Cycle Tracker", icon: "🌙" },
  { to: "/pregnancy-tracker", label: "Pregnancy Tracker", icon: "🤰" },
];

export default function AppLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [navOpen, setNavOpen] = useState(false);

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="app-shell">
      <button
        className="nav-toggle"
        onClick={() => setNavOpen((v) => !v)}
        aria-label="Toggle navigation"
      >
        ☰
      </button>

      <aside className={`sidebar ${navOpen ? "open" : ""}`}>
        <div className="sidebar-brand">
          <span className="brand-mark">◆</span>
          <span>Her Health</span>
        </div>

        <nav className="sidebar-nav">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) => `sidebar-link ${isActive ? "active" : ""}`}
              onClick={() => setNavOpen(false)}
            >
              <span className="sidebar-icon">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-user" title={user?.email}>
            {user?.email || "Signed in"}
          </div>
          <button className="btn btn-ghost" onClick={handleLogout}>
            Log out
          </button>
        </div>
      </aside>

      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
}

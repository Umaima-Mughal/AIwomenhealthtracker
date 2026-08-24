import { NavLink, Outlet, useNavigate } from "react-router-dom";  // cv
import { useState } from "react";
import {
  Activity,
  Baby,
  CalendarDays,
  HeartPulse,
  LayoutDashboard,
  MessageCircle,
  Microscope,
  Moon,
  Stethoscope,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

const NAV_ITEMS = [    // cv
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/tracking", label: "Tracking", icon: Activity },
  { to: "/chat", label: "AI Chat", icon: MessageCircle },
  { to: "/history", label: "3-Month History", icon: CalendarDays },
  { to: "/doctor-summary", label: "Doctor Summary", icon: Stethoscope },
  { to: "/pcos-checker", label: "PCOS Checker", icon: Microscope },
  { to: "/symptom-checker", label: "Symptom Checker", icon: HeartPulse },
  { to: "/cycle-tracker", label: "Cycle Tracker", icon: Moon },
  { to: "/pregnancy-tracker", label: "Pregnancy Tracker", icon: Baby },
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
            {NAV_ITEMS.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) => `sidebar-link ${isActive ? "active" : ""}`}
                onClick={() => setNavOpen(false)}
              >
                <Icon className="sidebar-icon" aria-hidden="true" />
                {item.label}
              </NavLink>
            );
          })}
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

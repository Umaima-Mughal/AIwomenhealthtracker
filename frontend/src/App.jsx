import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import AppLayout from "./layouts/AppLayout";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Tracking from "./pages/Tracking";
import Chat from "./pages/Chat";
import History from "./pages/History";
import DoctorSummary from "./pages/DoctorSummary";
import PCOSChecker from "./pages/PCOSChecker";
import SymptomChecker from "./pages/SymptomChecker";
import CycleTracker from "./pages/CycleTracker";
import PregnancyTracker from "./pages/PregnancyTracker";

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        <Route
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/" element={<Dashboard />} />
          <Route path="/tracking" element={<Tracking />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/history" element={<History />} />
          <Route path="/doctor-summary" element={<DoctorSummary />} />
          <Route path="/pcos-checker" element={<PCOSChecker />} />
          <Route path="/symptom-checker" element={<SymptomChecker />} />
          <Route path="/cycle-tracker" element={<CycleTracker />} />
          <Route path="/pregnancy-tracker" element={<PregnancyTracker />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}

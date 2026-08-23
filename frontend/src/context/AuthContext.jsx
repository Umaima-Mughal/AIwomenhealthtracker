import { createContext, useContext, useState, useCallback } from "react";
import * as api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(api.getStoredUser());
  const [isAuthenticated, setIsAuthenticated] = useState(api.isAuthenticated());

  const login = useCallback(async (email, password) => {
    const data = await api.login(email, password);
    setUser(data.user || null);
    setIsAuthenticated(true);
    return data;
  }, []);

  const signup = useCallback(async (email, password) => {
    return api.signup(email, password);
  }, []);

  const logout = useCallback(() => {
    api.logout();
    setUser(null);
    setIsAuthenticated(false);
  }, []);

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}

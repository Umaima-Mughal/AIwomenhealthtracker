import axios from "axios";

// Single configurable backend URL — never hardcode it in components.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach the Bearer token to every outgoing request automatically.
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Normalize errors into a consistent shape the UI can rely on.
function normalizeError(error) {
  if (!error.response) {
    return {
      status: 0,
      message: "Network error — could not reach the server. Check your connection or that the backend is running.",
    };
  }

  const { status, data } = error.response;

  if (status === 401) {
    // Session is invalid/expired — clear it so the app can redirect to login.
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    return { status, message: "Your session has expired. Please log in again." };
  }

  if (status === 422) {
    const detail = data?.detail;
    const message = Array.isArray(detail)
      ? detail.map((d) => d.msg).join(", ")
      : detail || "Some fields are invalid. Please check your input.";
    return { status, message };
  }

  if (status >= 500) {
    return { status, message: "Something went wrong on the server. Please try again shortly." };
  }

  return { status, message: data?.detail || data?.message || "Request failed." };
}

client.interceptors.response.use(
  (response) => response,
  (error) => Promise.reject(normalizeError(error))
);

// ---------------------------------------------------------------------------
// Auth
// ---------------------------------------------------------------------------

export async function signup(email, password) {
  const { data } = await client.post("/auth/signup", { email, password });
  return data;
}

export async function login(email, password) {
  const { data } = await client.post("/auth/login", { email, password });
  if (data.access_token) {
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token || "");
    localStorage.setItem("user", JSON.stringify(data.user || null));
  }
  return data;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
}

export function getStoredUser() {
  try {
    return JSON.parse(localStorage.getItem("user"));
  } catch {
    return null;
  }
}

export function isAuthenticated() {
  return Boolean(localStorage.getItem("access_token"));
}

// ---------------------------------------------------------------------------
// Tracking
// ---------------------------------------------------------------------------

export async function getTrackingHistory() {
  const { data } = await client.get("/tracking/");
  return data;
}

export async function createTracking(payload) {
  const { data } = await client.post("/tracking/", payload);
  return data;
}

// ---------------------------------------------------------------------------
// Chat
// ---------------------------------------------------------------------------

export async function getChatHistory() {
  const { data } = await client.get("/chat/");
  return data;
}

export async function sendChatMessage(message) {
  const { data } = await client.post("/chat/", { message });
  return data;
}

// ---------------------------------------------------------------------------
// PCOS
// ---------------------------------------------------------------------------

export async function checkPCOS(payload) {
  const { data } = await client.post("/pcos/", payload);
  return data;
}

// ---------------------------------------------------------------------------
// Pregnancy
// ---------------------------------------------------------------------------

export async function trackPregnancy(lmpDate) {
  const { data } = await client.post("/pregnancy/", { lmp_date: lmpDate });
  return data;
}

// ---------------------------------------------------------------------------
// Symptoms
// ---------------------------------------------------------------------------

export async function checkSymptoms(symptoms) {
  const { data } = await client.post("/symptoms/", { symptoms });
  return data;
}

// ---------------------------------------------------------------------------
// Cycle
// ---------------------------------------------------------------------------

export async function trackCycle(payload) {
  const { data } = await client.post("/cycle/", payload);
  return data;
}

// ---------------------------------------------------------------------------
// History / Doctor summary
// ---------------------------------------------------------------------------

export async function getThreeMonthHistory() {
  const { data } = await client.get("/history/3-months");
  return data;
}

export async function getDoctorSummary() {
  const { data } = await client.get("/doctor/summary");
  return data;
}

export default client;

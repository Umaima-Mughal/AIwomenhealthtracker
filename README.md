# 🌸 AI Women's Health Tracker

A full-stack **AI and Machine Learning platform for women's health** — a React frontend backed by a FastAPI API, Supabase (Auth + PostgreSQL), and a set of specialized AI/ML modules for chat, PCOS screening, symptom exploration, pregnancy tracking, and menstrual cycle tracking.

The project combines **Retrieval-Augmented Generation (RAG), a trained Machine Learning classifier, structured health knowledge matching, and deterministic date-based tracking** — using a different, purpose-built technique for each workflow instead of one general-purpose model for everything.

> ⚠️ **Medical Disclaimer:** This application is intended for educational and informational purposes only. It does not diagnose medical conditions and should not replace consultation, examination, or treatment by a qualified healthcare professional.

---

## 📑 Table of Contents

- [Screenshots](#-screenshots)
- [Architecture](#-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Backend Setup](#1-backend-setup)
  - [Frontend Setup](#2-frontend-setup)
- [Environment Variables](#-environment-variables)
- [API Reference](#-api-reference)
- [Training the PCOS Model](#-training-the-pcos-model)
- [Original Gradio MVP](#-original-gradio-mvp)
- [Limitations](#-limitations)
- [Roadmap](#-roadmap)
- [Author](#-author)

---

## 📸 Screenshots

| Login | Dashboard |
|---|---|
| <img width="1513" height="834" alt="image" src="https://github.com/user-attachments/assets/572fe550-ded3-483a-b9d4-64d7885166a0" />
| <img width="1858" height="880" alt="image" src="https://github.com/user-attachments/assets/569a16ac-039f-4d72-b2e6-69c7701150f4" />
 |

| Tracking | AI Chat |
|---|---|
|<img width="1821" height="868" alt="image" src="https://github.com/user-attachments/assets/668d471f-6667-423a-8e1f-cefc89f37313" />
 | <img width="1879" height="867" alt="AI Chat" src="https://github.com/user-attachments/assets/3910d4db-e253-4ed9-af3b-9b04ad2426d8" /> |

| PCOS Checker | Doctor Summary |
|---|---|
| <img width="1860" height="872" alt="image" src="https://github.com/user-attachments/assets/f39eae2e-fdbc-4101-a4c5-591c46cd9c9b" />
 | <img width="1874" height="859" alt="image" src="https://github.com/user-attachments/assets/0fc22c59-e0d1-473e-9225-c87e66b8abbf" />
 |

---

## 🏗️ Architecture

```text
Browser
   │
   ▼
React (Vite) Frontend  ──────────────►  FastAPI Backend  ──────────────►  Supabase (Auth + PostgreSQL)
   │  Bearer token on every                  │                                   │
   │  protected request                      │                                   │
   │                                          ▼                                   │
   │                                 AI / ML Modules                             │
   │                                 ├─ RAG Medical Chatbot (LangChain + FAISS)  │
   │                                 ├─ PCOS Risk Checker (Random Forest)        │
   │                                 ├─ Symptom Checker (structured matching)    │
   │                                 ├─ Pregnancy Tracker (date-based)           │
   │                                 └─ Cycle Tracker (date-based)               │
   └───────────────────────────────────────────────────────────────────────────┘
```

- **Frontend** — React + Vite SPA. Talks to the backend only through a single configurable `VITE_API_BASE_URL`; no secrets or Supabase keys live in the browser.
- **Backend** — FastAPI, the single source of truth for business logic, auth, and data access.
- **Auth** — Supabase Auth issues an access token on login; the frontend stores it and sends it as `Authorization: Bearer <token>` on every protected request.
- **Data** — Supabase-hosted PostgreSQL, accessed through SQLAlchemy models for user accounts, tracking records, chat messages, and planned insights/notifications functionality.
- **AI/ML** — Each health workflow is its own module under `modules/`, called directly by the relevant FastAPI route.

---

## ✨ Features

### 🖥️ Full-Stack Web App

- Email/password **signup & login** via Supabase Auth, with the session token stored client-side and attached automatically to protected requests.
- **Dashboard** summarizing recent tracking entries, cycle day, mood, and sleep, with quick actions to every tool.
- **Tracking** — log date, symptoms, mood, sleep hours, weight, cycle day, period status, and notes; view full history.
- **AI Chat** — a persistent conversation with the health chatbot, backed by real chat history stored per user.
- **3-Month History** — tracking records and chat messages from the last 90 days, with graceful empty states (no fabricated data).
- **Doctor Summary** — an auto-generated, shareable summary of detected patterns across your tracked data, meant to support (not replace) a conversation with a healthcare professional.
- **PCOS Checker**, **Symptom Checker**, **Cycle Tracker**, and **Pregnancy Tracker** — each backed by its dedicated AI/ML module below.

### 🤖 AI Women's Health Chatbot (RAG)

A women's health-focused chatbot built using a **Retrieval-Augmented Generation (RAG)** pipeline.

1. Medical information is loaded from CSV datasets.
2. Dataset rows are converted into LangChain documents and split into chunks with `RecursiveCharacterTextSplitter`.
3. Sentence embeddings are generated with a Hugging Face embedding model.
4. FAISS stores and retrieves the embedded medical knowledge via similarity search.
5. Retrieved context is passed to a Hugging Face-hosted language model (`HuggingFaceH4/zephyr-7b-beta`), which generates a concise, educational response.

The chatbot is instructed to stay on women's-health topics, avoid definite diagnoses, and keep responses short and educational. Chat history is persisted per authenticated user via the `/chat/` endpoint.

### 🧪 Machine Learning-Based PCOS Risk Checker

A trained **Random Forest Classifier** performs a pattern-based assessment from 13 health/lifestyle indicators (age, weight, height, BMI, cycle regularity, cycle length, weight gain, hair growth, skin darkening, hair loss, pimples, fast food intake, exercise). BMI is calculated automatically from height and weight.

**Training pipeline** (`train_pcos_model.py`): load the PCOS dataset → select the 13 features → 80/20 train/test split → train a 100-estimator Random Forest → evaluate accuracy, classification report, confusion matrix, and feature importance → save with Joblib to `models/pcos_model.pkl`.

The API returns a prediction label, the raw value, and the model's confidence — **not** a medical probability of having PCOS. Results should always be paired with professional evaluation.

### 🔎 Structured Symptom Checker

Compares user-entered symptoms against a structured JSON knowledge base of roughly 100 conditions, each with a name, category, description, and common symptoms.

Matching combines exact and similarity-based matching (Python's `SequenceMatcher`), scores each condition, and returns up to four ranked possible matches with matched symptoms and a description — never a diagnosis.

### 🤰 Pregnancy Journey Tracker

Estimates pregnancy progress from a **Last Menstrual Period (LMP)** date: current week, days pregnant, trimester, and estimated due date (standard 280-day duration). Week-specific data (baby size, development, maternal changes, recommendations) is pulled from `data/pregnancy_data.json` for weeks 1–42.

### 🩸 Menstrual Cycle Tracker

From LMP date, average cycle length, and period duration, estimates the next period date, current cycle day, and cycle phase (Menstrual, Follicular, Ovulation, Luteal). Cycle length is validated against the typical 21–35 day range.

> Every screening/tracking module above returns **estimates and pattern-based signals only**. None of them constitute a diagnosis — see [Limitations](#-limitations).

---

## 🛠️ Tech Stack

**Frontend**
| | |
|---|---|
| React 18 | UI library |
| Vite | Dev server & build tool |
| React Router | Client-side routing |
| Axios | HTTP client with interceptors for auth + error handling |

**Backend**
| | |
|---|---|
| FastAPI | REST API framework |
| SQLAlchemy | ORM over PostgreSQL |
| Pydantic | Request/response validation |
| Supabase (Auth + Postgres) | Authentication & data storage |
| Uvicorn | ASGI server |

**AI / ML**
| | |
|---|---|
| LangChain + LangChain Community | RAG orchestration |
| FAISS | Vector similarity search |
| Sentence Transformers / Hugging Face Embeddings | Text embeddings |
| Hugging Face Inference API (`zephyr-7b-beta`) | Chat generation |
| Scikit-learn (Random Forest) | PCOS classification |
| Pandas / NumPy / Joblib / Matplotlib | Data prep, model persistence, evaluation |

**Original MVP**
| | |
|---|---|
| Gradio | Standalone single-file interface (`gradio_app.py`), still included and runnable |

---

## 📂 Project Structure

```text
AIwomenhealthtracker/
│
├── backend/
│   └── app/
│       ├── main.py                # FastAPI app, CORS, router registration
│       ├── core/                  # config, database session, auth dependency
│       ├── api/                   # one router per feature (auth, tracking, chat,
│       │                          #   pcos, pregnancy, symptoms, cycle, history, doctor, health)
│       ├── db_models/             # SQLAlchemy models (User, Tracking, ChatMessage, Insight, Notification)
│       ├── services/              # health_history.py — 3-month aggregation & pattern analysis
│       └── supabase_client.py     # Supabase client used by auth
│
├── frontend/
│   ├── src/
│   │   ├── components/            # Shared UI: layout pieces, loading/empty/error states
│   │   ├── pages/                 # Dashboard, Tracking, Chat, History, DoctorSummary,
│   │   │                          #   PCOSChecker, SymptomChecker, CycleTracker, PregnancyTracker, Login, Signup
│   │   ├── layouts/AppLayout.jsx  # Sidebar navigation shell for authenticated pages
│   │   ├── services/api.js        # Centralized Axios client, one function per backend endpoint
│   │   ├── hooks/useApi.js        # Shared loading/error/data hook
│   │   ├── context/AuthContext.jsx# Session state (token, user, login/signup/logout)
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── modules/                       # AI/ML modules shared by both the FastAPI backend and Gradio MVP
│   ├── medical_chatbot.py         # RAG chatbot
│   ├── pcos_checker.py            # PCOS model inference
│   ├── symptom_checker.py         # Symptom matching
│   ├── pregnancy_tracker.py       # Pregnancy calculations
│   └── cycle_tracker.py           # Cycle calculations
│
├── data/                          # CSV/JSON datasets used by the AI/ML modules
├── models/pcos_model.pkl          # Trained Random Forest model
├── gradio_app.py                  # Original standalone Gradio MVP
├── train_pcos_model.py            # PCOS model training script
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- A [Supabase](https://supabase.com) project (URL + anon key) and a Postgres `DATABASE_URL`

### 1. Backend Setup

```bash
# from the repository root
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the repository root (see [Environment Variables](#-environment-variables) for the full list), then run the API **from the repository root** (it's imported as `backend.app.main`):

```bash
uvicorn backend.app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`

### 2. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env   # adjust VITE_API_BASE_URL if your backend runs elsewhere
npm run dev
```

- Frontend: `http://localhost:5173`

Open `http://localhost:5173`, sign up, log in, and use the sidebar to reach every page.

---

## 🔐 Environment Variables

**Backend** — `.env` in the repository root (read by `backend/app/core/config.py`):

```env
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
SUPABASE_URL=https://<your-project>.supabase.co
SUPABASE_KEY=<your-supabase-anon-key>
HF_TOKEN=<your-hugging-face-token>

# Optional — comma-separated list of origins allowed to call the API from a browser.
# Defaults to the local Vite dev server if omitted.
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**Frontend** — `frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

> ⚠️ Only the Supabase **anon/public** key belongs in `SUPABASE_KEY` — never a service-role key. The frontend never stores or receives any Supabase key; it only ever talks to your own FastAPI backend and holds the user's access token in local storage. Never commit a real `.env` file, API keys, or access tokens.

---

## 📡 API Reference

All endpoints except `/`, `/db-test`, `/health`, `/auth/signup`, and `/auth/login` require `Authorization: Bearer <access_token>`.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/signup` | Create a Supabase account |
| `POST` | `/auth/login` | Log in, returns access + refresh tokens |
| `GET` | `/tracking/` | List the current user's tracking entries |
| `POST` | `/tracking/` | Create a tracking entry |
| `GET` | `/chat/` | Get chat history |
| `POST` | `/chat/` | Send a message, get an AI response |
| `POST` | `/pcos/` | Run the PCOS risk checker |
| `POST` | `/pregnancy/` | Get pregnancy tracking results from an LMP date |
| `POST` | `/symptoms/` | Match free-text symptoms against the knowledge base |
| `POST` | `/cycle/` | Get menstrual cycle tracking results |
| `GET` | `/history/3-months` | Tracking records and chat history from the last 90 days |
| `GET` | `/doctor/summary` | Auto-generated pattern summary of the last 3 months |
| `GET` | `/health` | Service health check |
| `GET` | `/db-test` | Verifies the database connection |

Full request/response schemas are available at `/docs` once the backend is running.

---

## 🧠 Training the PCOS Model

```bash
python train_pcos_model.py
```

Loads the PCOS dataset → selects the model's input features → splits into training/testing sets → trains the Random Forest classifier → prints accuracy, classification report, and confusion matrix → saves the model to `models/pcos_model.pkl` → displays a feature-importance chart.

---

## 🖥️ Original Gradio MVP

Before the full-stack migration, the project shipped as a single-file **Gradio Blocks** app (`gradio_app.py`) with five tabs — Chatbot, PCOS Checker, Symptom Checker, Pregnancy Tracker, and Cycle Tracker — built on the same `modules/` used by the FastAPI backend today. It's kept in the repo and still runs standalone:

```bash
python gradio_app.py
```

Gradio will print a local URL to open in your browser.

---

## ⚠️ Limitations

- The application cannot diagnose medical conditions.
- PCOS assessment is limited to the selected model features and patterns learned from the training dataset; high model accuracy does not equal clinical diagnostic accuracy.
- Symptom matching depends on the conditions available in the JSON knowledge base and may not understand every natural-language description.
- Pregnancy and cycle calculations are simple, date-based estimates — actual gestational age, due dates, and cycle phases vary between individuals.
- AI-generated chat responses may be incomplete or inaccurate.
- None of the above replace laboratory tests, physical examination, imaging, or clinical evaluation by a qualified healthcare professional.

---

## 🗺️ Roadmap

- [x] Migrate the Gradio MVP to a React frontend + FastAPI backend.
- [x] Authenticated user profiles and persistent, user-specific health history (Supabase).
- [x] 3-month history and doctor-summary pattern detection across tracking and chat data.
- [ ] Add dedicated insights and notification functionality.
- [ ] Connect relevant historical records more deeply across independent health workflows.
- [ ] Improve natural-language symptom normalization and medical terminology mapping.
- [ ] Improve RAG retrieval quality, source filtering, and retrieval evaluation.
- [ ] Add automated unit and integration tests for backend and frontend.
- [ ] Improve menstrual cycle phase estimation.
- [ ] Deploy the platform as a publicly accessible web application.

Future development continues to prioritize **responsible AI boundaries, transparent system limitations, and modular architecture**.

---

## 👩‍💻 Author

**Umaima Mughal**
Software Engineering Student — interested in Artificial Intelligence, Machine Learning, Generative AI, and Software Development.

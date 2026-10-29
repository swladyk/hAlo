# CLAUDE.md

Shared instructions for every coding agent working in this repo.
Our 4-person team builds an AI-agent MVP during a hackathon. Each person works with their own coding agent, in parallel, on separate features. **Read this file fully before every task.**

---

## 1. Stack (do not change without team agreement)

| Layer | Tech | Hosting |
|---|---|---|
| Frontend | React + Vite + TypeScript + Tailwind CSS + shadcn/ui | Vercel |
| Backend | Python 3.12 + FastAPI + SQLModel + Uvicorn | Render (free web service) |
| Database | Postgres on Neon (`main` branch = live app, one branch per developer); SQLite allowed as local fallback | Neon |
| LLM | Called **only from the backend**, through `backend/app/llm.py` | — |
| CI | GitHub Actions (lint + build + tests on every PR) | GitHub |

No Docker, no Next.js, no extra frameworks or state-management libraries unless the team agrees. Don't add a dependency when a few lines of code will do.

---

## 2. Repo structure

```
/
├── CLAUDE.md
├── README.md                 # how to run locally + deploy steps
├── render.yaml               # Render blueprint for the backend
├── .github/workflows/ci.yml
├── frontend/
│   ├── .env.example
│   ├── vite.config.ts        # dev proxy: /api -> http://localhost:8000
│   └── src/
│       ├── main.tsx
│       ├── App.tsx           # layout + routing only
│       ├── lib/api.ts        # the ONLY place that builds API URLs / fetches
│       ├── components/ui/    # shadcn/ui components (shared)
│       └── features/
│           └── <feature>/    # each feature's components, hooks, types
└── backend/
    ├── .env.example
    ├── requirements.txt
    ├── seed.py               # fills the DB with demo data
    ├── tests/
    └── app/
        ├── main.py           # creates app, CORS, includes feature routers
        ├── config.py         # settings from environment variables
        ├── db.py             # engine, session, create_all
        ├── llm.py            # the ONLY place that calls an LLM provider
        └── features/
            └── <feature>/
                ├── router.py # FastAPI APIRouter, mounted under /api/<feature>
                ├── models.py # SQLModel tables, prefixed with the feature name
                └── service.py
```

---

## 3. Team rules for agents

1. **Stay in your feature folders.** Only edit `frontend/src/features/<your-feature>/` and `backend/app/features/<your-feature>/`.
2. **Shared files** (`app/main.py`, `App.tsx`, `lib/api.ts`, `db.py`, `llm.py`, `config.py`, `requirements.txt`, `package.json`, `components/ui/`): make only the **minimal** change needed, such as one line to register your router or route. Never refactor them as a side effect.
3. **Never change another feature's code, tables or API** without being explicitly told the team agreed.
4. **API contracts:** every endpoint lives under `/api/<feature>/...`, uses Pydantic/SQLModel schemas for request and response, and appears in the FastAPI OpenAPI docs (`/docs`). Don't rename or remove fields that another feature uses.
5. **DB tables:** prefix table names with the feature name (e.g. `feed_posts`). Don't modify another feature's tables.
6. **Secrets:** never hardcode API keys, URLs or passwords. Read them from environment variables via `config.py` (backend) or `import.meta.env` (frontend). Add every new variable to the matching `.env.example` with a placeholder value. Never commit `.env`.
7. **LLM calls go only through `backend/app/llm.py`.** The frontend never calls an LLM provider directly.
8. **Keep it simple.** This is an MVP for a demo. Prefer readable code over abstractions. No premature optimization.
9. **The UI must be responsive** (works on a phone) and use shadcn/ui + Tailwind, not custom CSS files.
10. **Before finishing a task:** run the frontend build, backend lint and tests (commands in section 6) and fix anything you broke.
11. **When you change something shared** (contract, table, env var, dependency), state it clearly in your final summary so the human can announce it to the team.

---

## 4. Environment variables

**backend/.env.example**
```
DATABASE_URL=sqlite:///./app.db          # local fallback; use your Neon branch URL for Postgres
FRONTEND_ORIGINS=http://localhost:5173   # comma-separated list of allowed CORS origins
LLM_API_KEY=                             # empty = mock mode (fake streamed reply)
LLM_MODEL=                               # model name for the chosen provider
```

**frontend/.env.example**
```
VITE_API_URL=                            # empty locally (Vite proxy); Render backend URL in production
```

Notes:
- Neon gives URLs like `postgresql://...?sslmode=require`. `db.py` must normalize them for SQLAlchemy with the psycopg driver (`postgresql+psycopg://...`) and keep `sslmode=require`.
- If `LLM_API_KEY` is empty, `llm.py` returns a fake streamed answer, so the app works without keys (useful for CI and new teammates).

---

## 5. Backend conventions

- `app/main.py` creates the FastAPI app, configures CORS from `FRONTEND_ORIGINS`, calls `create_all` on startup and includes each feature router with `prefix="/api/<feature>"`.
- Use SQLModel for tables and schemas. Tables are created automatically with `SQLModel.metadata.create_all` (no migrations during the hackathon). Write SQL that works on both SQLite and Postgres.
- Streaming responses (LLM output, agent steps) use **Server-Sent Events** via `StreamingResponse` with `media_type="text/event-stream"`.
- `llm.py` exposes a small async interface, e.g. `async def stream_chat(messages: list[dict]) -> AsyncIterator[str]`. Swapping provider or model happens only here.
- Agent loops must have a maximum number of steps.
- Don't write files to the backend's local disk. Render's filesystem is wiped on every deploy and restart.
- Tests: `pytest` + FastAPI `TestClient`, using an in-memory SQLite DB and LLM mock mode.

## 6. Frontend conventions

- All backend calls go through `src/lib/api.ts`, which prefixes paths with `import.meta.env.VITE_API_URL ?? ""`. Locally the Vite dev proxy forwards `/api` to `http://localhost:8000`.
- Use shadcn/ui components from `src/components/ui/`. Install new ones with the shadcn CLI.
- Each feature exports one top-level page or component that `App.tsx` mounts. One line per feature.
- Stream LLM responses by reading the SSE stream with `fetch` + `ReadableStream`, and show text as it arrives.
- Use TypeScript types for every API response, matching the backend schemas.

## 7. Commands

| Task | Command |
|---|---|
| Backend install | `cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` |
| Backend run | `cd backend && uvicorn app.main:app --reload --port 8000` |
| Backend lint | `cd backend && ruff check .` |
| Backend tests | `cd backend && pytest` |
| Seed demo data | `cd backend && python seed.py` |
| Frontend install | `cd frontend && npm install` |
| Frontend run | `cd frontend && npm run dev` (http://localhost:5173) |
| Frontend lint | `cd frontend && npm run lint` |
| Frontend build | `cd frontend && npm run build` |

## 8. Git workflow

- Branch from fresh `main`: `feat/<feature-name>`.
- Small commits. Open a PR to `main`; CI must be green before merging.
- Before merging: `git pull origin main`, resolve conflicts **without changing other features' behavior**, then run the app, lint and tests.
- Every merge to `main` auto-deploys the frontend to Vercel and the backend to Render.

## 9. Deployment

- **Vercel (frontend):** root directory `frontend`, framework Vite, build `npm run build`, output `dist`. Env var: `VITE_API_URL=<Render backend URL>`.
- **Render (backend):** web service from `render.yaml`, root directory `backend`, build `pip install -r requirements.txt`, start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, health check `/api/health`. Env vars: `DATABASE_URL` (Neon `main` branch), `FRONTEND_ORIGINS` (Vercel URL), `LLM_API_KEY`, `LLM_MODEL`.
- **Neon:** `main` branch for production, branches `dev-<name>` for each developer.
- The Render free tier sleeps after ~15 min idle. The first request can take up to a minute, so wake it before demos.

---

## 10. BOOTSTRAP TASK: build the "Hello World" skeleton

> Do this task once, when the repo is empty. Delete this section after the skeleton is merged.

Build the complete skeleton described above, with three demo features that prove every layer works end to end. Keep each feature minimal.

**Feature `health`**
- Backend: `GET /api/health` → `{"status": "ok", "db": "ok" | "error", "llm": "live" | "mock"}`. It runs a trivial DB query to check the connection.
- Frontend: a status card at the top of the page showing backend, DB and LLM status, with green and red badges.

**Feature `hello`** (DB round trip)
- Backend: table `hello_messages` (id, text, created_at). `GET /api/hello/messages` lists the newest first; `POST /api/hello/messages` with `{"text": "..."}` creates one.
- Frontend: an input + button to add a message and a list of saved messages.
- `seed.py` inserts 3 example messages if the table is empty.

**Feature `chat`** (LLM streaming)
- Backend: `POST /api/chat/stream` with `{"messages": [{"role": "user", "content": "..."}]}` streams the reply as SSE via `llm.stream_chat`. In mock mode it streams a fake reply word by word.
- Frontend: a simple chat box with a message list and an input that shows the assistant reply token by token as it streams.

**Also create:**
- `frontend/` and `backend/` set up per sections 2–6, including the Vite proxy, Tailwind, shadcn/ui (at least button, input, card, badge), `lib/api.ts`, `config.py`, `db.py` with Neon URL normalization, and `llm.py` with mock mode.
- Both `.env.example` files, plus a root `.gitignore` covering `.env`, `.venv`, `node_modules`, `dist` and `*.db`.
- `render.yaml` for the backend web service (free plan, health check `/api/health`).
- `.github/workflows/ci.yml`, running on pull requests and pushes to `main`, with two jobs:
  - frontend: `npm ci`, `npm run lint`, `npm run build`
  - backend: install deps, `ruff check .`, `pytest`
- `backend/tests/` with tests for health, hello (create + list) and chat (mock stream returns text).
- `README.md` covering: local setup, the commands from section 7, and step-by-step deploy instructions for Neon, Render and Vercel (which env var goes where).

**Done when:**
1. `npm run build`, `npm run lint`, `ruff check .` and `pytest` all pass.
2. Running backend and frontend locally shows: the health card all green (LLM may show "mock"), adding a message persists across a page reload, and chat streams a reply.
3. The app works with both `DATABASE_URL=sqlite:///./app.db` and a Neon Postgres URL.
4. Finish with a short summary: files created, how to run them, and what the human must configure manually (Neon branches, Render service, Vercel project, env vars).

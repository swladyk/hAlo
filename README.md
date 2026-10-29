# hAlo

AI-agent MVP built at a hackathon by a 4-person team.

- **Frontend:** Node 24, React, Vite, TypeScript, Tailwind, shadcn/ui → Vercel
- **Backend:** Python 3.14, FastAPI, SQLModel → Render
- **Database:** Postgres on Neon (SQLite works locally)
- **LLM:** OpenAI, called only from `backend/app/llm.py` (mock mode when there's no key)

Coding agents: read [`CLAUDE.md`](CLAUDE.md). Project skills are in [`.claude/skills/`](.claude/skills).

The skeleton ships with three demo features:

| Feature | Backend | Frontend |
|---|---|---|
| `health` | `GET /api/health` | status card |
| `hello` | `GET`/`POST /api/hello/messages` | message form and list (DB round trip) |
| `chat` | `POST /api/chat/stream` (SSE) | chat box that streams replies |

API docs are at http://localhost:8000/docs when the backend is running.

## Local setup

### 0. Install the tools (once per laptop)

You need **uv** (it installs Python 3.14 for you), plus **nvm** to install **Node 24**, which comes with npm.

**uv**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh     # macOS / Linux (on macOS, `brew install uv` also works)
# Windows (PowerShell): powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**nvm**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash     # macOS / Linux
# Windows: use WSL, or nvm-windows (https://github.com/coreybutler/nvm-windows)
```

**Node 24 + npm**
```bash
nvm install 24
nvm alias default 24
```

Open a **new terminal**, then check:
```bash
uv --version     # uv 0.x
node -v          # v24.x
npm -v           # 11.x or newer
```
If `uv` or `nvm` is still "command not found", run `source ~/.bashrc` (or `source ~/.zshrc` on macOS), or restart the terminal.

### 1. Run the app

```bash
# Backend (terminal 1)
cd backend
uv sync                       # creates .venv with Python 3.14 + all deps from uv.lock
cp .env.example .env          # the defaults work: SQLite + LLM mock mode
uv run python seed.py
uv run uvicorn app.main:app --reload --port 8000

# Frontend (terminal 2)
cd frontend
npm install
cp .env.example .env          # leave VITE_API_URL empty locally
npm run dev                   # http://localhost:5173
```

To use real Postgres, put your Neon branch URL in `backend/.env` as `DATABASE_URL`. To get real LLM replies, set `LLM_API_KEY` (and optionally `LLM_MODEL`; the default is `gpt-4o-mini`).

## Commands

| Task | Command |
|---|---|
| Backend install | `cd backend && uv sync` |
| Backend run | `cd backend && uv run uvicorn app.main:app --reload --port 8000` |
| Backend lint | `cd backend && uv run ruff check .` |
| Backend tests | `cd backend && uv run pytest` |
| Seed demo data | `cd backend && uv run python seed.py` |
| Frontend install | `cd frontend && npm install` |
| Frontend run | `cd frontend && npm run dev` (http://localhost:5173) |
| Frontend lint | `cd frontend && npm run lint` |
| Frontend build | `cd frontend && npm run build` |

Add a Python package with `cd backend && uv add <pkg>` (`uv add --dev <pkg>` for dev tools) and commit `pyproject.toml` + `uv.lock`. Don't use pip.

CI (`.github/workflows/ci.yml`) runs frontend lint and build, plus backend ruff and pytest, on every PR and every push to `main`.

## Deployment

Every merge to `main` auto-deploys the frontend to Vercel and the backend to Render. Do the one-time setup in this order:

### 1. Neon (database)
1. Create a project at https://console.neon.tech (Postgres, in a region close to the Render region).
2. The default branch `main` is production. Copy its connection string (`postgresql://...?sslmode=require`).
3. Create one branch per developer: `dev-<name>`. Each developer puts their branch URL in their own `backend/.env` as `DATABASE_URL`.
4. Tables are created automatically on backend startup. To add demo data to a branch, run `uv run python seed.py` with that branch's `DATABASE_URL` set.

### 2. Render (backend)
1. In https://dashboard.render.com, go to **New → Blueprint** and connect this GitHub repo. Render reads `render.yaml` (free web service, root `backend`, health check `/api/health`).
2. Set these environment variables on the service:

   | Variable | Value |
   |---|---|
   | `DATABASE_URL` | Neon **`main`** branch connection string |
   | `FRONTEND_ORIGINS` | Your Vercel URL, e.g. `https://halo.vercel.app` (comma-separated if there are several) |
   | `LLM_API_KEY` | OpenAI API key (leave empty for mock mode) |
   | `LLM_MODEL` | e.g. `gpt-4o-mini` (optional) |
3. Deploy, then open `https://<service>.onrender.com/api/health` and check that you get `{"status":"ok","db":"ok",...}`.

### 3. Vercel (frontend)
1. In https://vercel.com/new, import this repo.
2. Set **Root Directory** to `frontend`, **Framework** to Vite, **Build Command** to `npm run build` and **Output** to `dist`.
3. Environment variable: `VITE_API_URL` = the Render backend URL, e.g. `https://halo-backend.onrender.com` (no trailing slash).
4. Deploy. Then make sure `FRONTEND_ORIGINS` on Render contains the final Vercel URL.

> The Render free tier sleeps after about 15 minutes idle, so the first request can take up to a minute. Open `/api/health` before a demo to wake it up.

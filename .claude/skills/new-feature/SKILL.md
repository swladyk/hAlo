---
name: new-feature
description: Scaffold a new hAlo feature end to end (FastAPI router/models/service + React feature folder + test). Use when starting any new feature, endpoint group, page or table in this repo.
---

# New feature: `<f>` (lowercase, one word or snake_case)

Copy the shape of `hello` — it is the reference feature (DB round trip). `chat` is the reference for streaming.

## Backend — `backend/app/features/<f>/`
1. `__init__.py` (empty).
2. `models.py` — SQLModel tables with `__tablename__ = "<f>_<things>"`, plus `<X>Create` / `<X>Read` schemas. See `app/features/hello/models.py`.
3. `service.py` — plain functions taking `session: Session`; all DB logic lives here.
4. `router.py` — `router = APIRouter()`; paths are relative (`"/items"`), every route has `response_model` (or a typed return), and uses `session: SessionDep` from `app.db`.
5. Shared-file edits (one line each, nothing else):
   - `app/main.py`: `app.include_router(<f>_router, prefix="/api/<f>", tags=["<f>"])` + its import.
   - `app/db.py` `create_db_and_tables`: `import app.features.<f>.models  # noqa: F401` (only if you added tables).
   - `tests/conftest.py`: the same models import, so test DBs get your tables.
6. `backend/tests/test_<f>.py` using the `client` fixture (in-memory SQLite, LLM mock).

## Frontend — `frontend/src/features/<f>/`
1. `types.ts` — TS types mirroring the backend `Read` schemas exactly (field names and types).
2. `<F>Page.tsx` (or `<F>Card.tsx`) — the single exported top-level component. Fetch only via `@/lib/api`.
3. `App.tsx`: one import + one `<FPage />` line. Nothing else.

## Rules
- Never edit another feature's folder, tables or API fields.
- New env var → `config.py` + `backend/.env.example` (or `import.meta.env` + `frontend/.env.example`).
- New dependency → only if a few lines of code won't do; backend via `uv add <pkg>`, frontend via `npm install <pkg>`; it's a shared change.
- Finish with the `preflight` skill and list every shared change in your summary.

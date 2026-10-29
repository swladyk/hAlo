---
name: preflight
description: The checks to run and the summary to write before finishing any task in hAlo. Use at the end of every coding task, before committing or opening a PR.
---

# Preflight

Run all four from the repo root and fix anything you broke (don't "fix" other features' failures — report them):

```bash
(cd backend && ruff check . && pytest)
(cd frontend && npm run lint && npm run build)
```
Backend venv: `source backend/.venv/bin/activate` first if `ruff`/`pytest` aren't on PATH.

If you touched UI or an endpoint, also run the app (`uvicorn app.main:app --reload --port 8000` + `npm run dev`) and try the change at phone width.

Self-check:
- [ ] Only my feature folders changed, plus one-line registrations in shared files.
- [ ] No secrets, URLs or keys hardcoded; new env vars are in `.env.example`.
- [ ] Tables prefixed `<feature>_`; no Postgres-only SQL.
- [ ] LLM only via `app/llm.py`; works in mock mode.

## Final summary template
```
What: <one or two lines>
Files: <list>
How to try: <commands / URL>
Checks: ruff ✅ pytest ✅ lint ✅ build ✅
Shared changes (announce to team): <API contract / table / env var / dependency / shared file — or "none">
```

---
name: fastapi-sqlmodel
description: Conventions for hAlo backend code — FastAPI routers, SQLModel tables/schemas, DB sessions, SQLite+Postgres compatibility and pytest. Use when writing or changing anything under backend/.
---

# Backend conventions (Python 3.14, FastAPI, SQLModel)

## Layout
`router.py` (HTTP only) → `service.py` (logic, DB) → `models.py` (tables + schemas). Mounted at `/api/<feature>` in `app/main.py`.

## Patterns
```python
# models.py
class TodoItem(SQLModel, table=True):
    __tablename__ = "todo_items"               # always prefix with feature name
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

class TodoItemCreate(SQLModel):                 # request schema
    title: str = Field(min_length=1, max_length=200)

class TodoItemRead(SQLModel):                   # response schema
    id: int
    title: str
    created_at: datetime

# router.py
@router.post("/items", response_model=TodoItemRead, status_code=201)
def create_item(body: TodoItemCreate, session: SessionDep):
    return service.create_item(session, body.title)
```
- Session: `from app.db import SessionDep` (Annotated dependency). Don't create engines in features.
- Settings: `from app.config import settings`. Never read `os.environ` directly; never hardcode secrets.
- Use `HTTPException(404, "...")` for missing rows.
- Order with `col(Model.field).desc()`; use `select()` — no raw SQL except trivial `SELECT 1`.

## DB rules
- Tables via `SQLModel.metadata.create_all` (no migrations). Changing a column on an existing table needs a new table name or a team-agreed DB reset — tell the human.
- Must run on SQLite **and** Postgres: no JSONB/ARRAY/Postgres-only functions; use `str`, `int`, `float`, `bool`, `datetime`; store JSON as `str` if needed.
- Neon URLs are normalized in `app/db.py` (`postgresql+psycopg://`, keeps `sslmode=require`).
- Never write files to local disk (Render wipes it).

## Tests
`tests/test_<feature>.py`, use the `client` fixture from `tests/conftest.py` (in-memory SQLite, LLM forced to mock). Register new tables there with an import. Run: `cd backend && ruff check . && pytest`.

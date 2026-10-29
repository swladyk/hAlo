from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from app.config import settings


def normalize_db_url(url: str) -> str:
    """Make Neon/Heroku style Postgres URLs use the psycopg (v3) driver. Query string is kept."""
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix) :]
    return url


def make_engine(url: str):
    url = normalize_db_url(url)
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url, pool_pre_ping=True)


engine = make_engine(settings.database_url)


def create_db_and_tables() -> None:
    # Import feature models so their tables are registered on SQLModel.metadata.
    import app.features.hello.models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


# Use in routes: def handler(session: SessionDep): ...
SessionDep = Annotated[Session, Depends(get_session)]

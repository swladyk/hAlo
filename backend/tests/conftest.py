import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import app.features.hello.models  # noqa: F401  (register tables)
from app.config import settings
from app.db import get_session
from app.main import app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(settings, "llm_api_key", "")  # force LLM mock mode
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    def override_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

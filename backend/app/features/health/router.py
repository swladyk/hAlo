from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import text

from app import llm
from app.db import SessionDep

router = APIRouter()


class HealthResponse(BaseModel):
    status: Literal["ok"]
    db: Literal["ok", "error"]
    llm: Literal["live", "mock"]


@router.get("", response_model=HealthResponse)
def health(session: SessionDep) -> HealthResponse:
    try:
        session.exec(text("SELECT 1"))
        db = "ok"
    except Exception:
        db = "error"
    return HealthResponse(status="ok", db=db, llm="live" if llm.is_live() else "mock")

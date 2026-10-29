from fastapi import APIRouter

from app.db import SessionDep
from app.features.hello import service
from app.features.hello.models import HelloMessageCreate, HelloMessageRead

router = APIRouter()


@router.get("/messages", response_model=list[HelloMessageRead])
def list_messages(session: SessionDep):
    return service.list_messages(session)


@router.post("/messages", response_model=HelloMessageRead, status_code=201)
def create_message(body: HelloMessageCreate, session: SessionDep):
    return service.create_message(session, body.text)

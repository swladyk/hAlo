from sqlmodel import Session, col, select

from app.features.hello.models import HelloMessage


def list_messages(session: Session, limit: int = 50) -> list[HelloMessage]:
    stmt = select(HelloMessage).order_by(col(HelloMessage.id).desc()).limit(limit)
    return list(session.exec(stmt))


def create_message(session: Session, text: str) -> HelloMessage:
    message = HelloMessage(text=text)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message

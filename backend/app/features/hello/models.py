from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class HelloMessageCreate(SQLModel):
    text: str = Field(min_length=1, max_length=500)


class HelloMessage(SQLModel, table=True):
    __tablename__ = "hello_messages"

    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(max_length=500)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class HelloMessageRead(SQLModel):
    id: int
    text: str
    created_at: datetime

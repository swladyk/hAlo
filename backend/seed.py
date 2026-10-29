"""Fill the DB with demo data. Safe to run multiple times."""

from sqlmodel import Session, select

from app.db import create_db_and_tables, engine
from app.features.hello.models import HelloMessage

DEMO_MESSAGES = [
    "Hello from hAlo!",
    "The database round trip works.",
    "Add your own message above.",
]


def main() -> None:
    create_db_and_tables()
    with Session(engine) as session:
        if session.exec(select(HelloMessage)).first():
            print("hello_messages already has data, skipping.")
            return
        for text in DEMO_MESSAGES:
            session.add(HelloMessage(text=text))
        session.commit()
        print(f"Inserted {len(DEMO_MESSAGES)} hello messages.")


if __name__ == "__main__":
    main()

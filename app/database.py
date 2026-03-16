"""
Database utility module for chat logs using SQLite.

This module defines the SQLAlchemy models and session factory
required to persist chat history. Each record captures the
user's question, the model's response and a timestamp.  Using
SQLite keeps the deployment lightweight while still supporting
SQL queries.  Should you wish to migrate to another relational
engine later on (e.g. MySQL or PostgreSQL), only the connection
string will need to change.

Usage:

    from .database import get_session, ChatLog, init_db
    init_db()
    with get_session() as db:
        db.add(ChatLog(question="Hello", answer="Hi!"))
        db.commit()

"""

from __future__ import annotations

import datetime
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Define the base class for declarative models
Base = declarative_base()


class ChatLog(Base):
    """ORM model representing a single chat exchange.

    Each chat log stores the question sent by the user, the
    response returned by the language model and the timestamp
    when the exchange occurred.  The primary key `id` is
    auto-incrementing.
    """

    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<ChatLog(id={self.id}, question={self.question[:20]!r}, answer={self.answer[:20]!r}, timestamp={self.timestamp})>"


# SQLite database URL.  When deploying with Docker this path
# resolves inside the container.  Feel free to customise via the
# DATABASE_URL environment variable in docker-compose.yml.
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/chat.db")

# Create an engine bound to the database URL.  `connect_args` is
# required for SQLite to allow multi-threaded access.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_session() -> Iterator[sessionmaker]:
    """Provide a transactional scope for database operations.

    This context manager yields a SQLAlchemy session and ensures
    that the session is properly closed afterwards.  It does not
    commit or rollback automatically—this should be handled by
    the caller.

    Usage:

        with get_session() as db:
            db.add(ChatLog(...))
            db.commit()

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
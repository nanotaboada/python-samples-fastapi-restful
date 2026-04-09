"""
Database setup and session management for async SQLAlchemy.

- Configures the async database engine from the DATABASE_URL environment
  variable (SQLite default, PostgreSQL compatible).
- Creates an async sessionmaker for ORM operations.
- Defines the declarative base class for model definitions.
- Provides an async generator dependency to yield database sessions.

Environment variables:
    DATABASE_URL: Full async database URL. Defaults to SQLite:
        sqlite+aiosqlite:///./players-sqlite3.db
    STORAGE_PATH: (legacy) SQLite file path. Ignored when DATABASE_URL is set.
"""

import logging
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


def get_database_url() -> str:
    """Return the async database URL from environment variables.

    Reads DATABASE_URL first; if unset, constructs a SQLite URL from
    STORAGE_PATH (defaulting to ./players-sqlite3.db).
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        storage_path = os.getenv("STORAGE_PATH", "./players-sqlite3.db")
        database_url = f"sqlite+aiosqlite:///{storage_path}"
    return database_url


DATABASE_URL: str = get_database_url()

_connect_args = (
    {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

logger = logging.getLogger("uvicorn")
logging.getLogger("sqlalchemy.engine.Engine").handlers = logger.handlers

async_engine = create_async_engine(DATABASE_URL, connect_args=_connect_args, echo=True)

async_sessionmaker = sessionmaker(
    bind=async_engine, class_=AsyncSession, autocommit=False, autoflush=False
)

Base = declarative_base()


async def generate_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to yield an async SQLAlchemy ORM session.

    Yields:
        AsyncSession: An instance of an async SQLAlchemy ORM session.
    """
    async with async_sessionmaker() as async_session:
        yield async_session

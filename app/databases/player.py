"""
Database setup and session management for async SQLAlchemy with SQLite.

- Configures the async database engine using `aiosqlite` driver.
- Creates an async sessionmaker for ORM operations.
- Defines the declarative base class for model definitions.
- Provides an async generator dependency to yield database sessions.

The `STORAGE_PATH` environment variable controls the SQLite file location.
"""

import logging
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

storage_path = os.getenv("STORAGE_PATH", "./storage/players-sqlite3.db")
DATABASE_URL = f"sqlite+aiosqlite:///{storage_path}"

logger = logging.getLogger("uvicorn")
logging.getLogger("sqlalchemy.engine.Engine").handlers = logger.handlers

async_engine = create_async_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

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

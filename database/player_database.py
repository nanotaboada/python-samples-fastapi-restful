# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------

import logging
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

database_file_path = os.getenv("DATABASE_FILE_PATH", "./sqlite3-db/players-sqlite3.db")
DATABASE_URL = f"sqlite+aiosqlite:///{database_file_path}"

logger = logging.getLogger("uvicorn")
logging.getLogger("sqlalchemy.engine.Engine").handlers = logger.handlers

async_engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)

async_sessionmaker = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
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

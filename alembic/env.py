"""
Alembic environment configuration for async SQLAlchemy.

Reads DATABASE_URL from the environment to support both SQLite (local dev/test)
and PostgreSQL (Docker/production). Uses render_as_batch=True for SQLite ALTER
TABLE compatibility (harmless on PostgreSQL).
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from databases.player_database import Base, get_database_url
from schemas.player_schema import Player  # noqa: F401 — registers ORM model with Base

# Supports both SQLite (local) and PostgreSQL (Docker, see #542):
#   sqlite+aiosqlite:///./players-sqlite3.db
#   postgresql+asyncpg://postgres:password@postgres:5432/playersdb
database_url = get_database_url()

config = context.config
config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no DB connection, generates SQL)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (against a live DB connection)."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

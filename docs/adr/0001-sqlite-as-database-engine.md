# ADR-0001: SQLite as Database Engine

Date: 2026-03-21

## Status

Accepted

## Context

This project is a proof-of-concept REST API. A database engine was
required to persist player data. The realistic alternatives were:

- **PostgreSQL** — the standard choice for production REST APIs; requires
  a running server process, a connection string, and either a local
  installation or a Docker service alongside the application.
- **MySQL / MariaDB** — similar trade-offs to PostgreSQL.
- **SQLite** — an embedded, file-based engine; no server process, no
  installation beyond a driver, and the database file can be committed
  to the repository pre-seeded.

The project includes a pre-seeded database file (`storage/players-sqlite3.db`)
that contains all 26 players from the Argentina 2022 World Cup squad.
SQLAlchemy 2.0 abstracts most engine-specific SQL, and aiosqlite provides
an async driver compatible with the rest of the async stack.

## Decision

We will use SQLite as the database engine via `aiosqlite` and
SQLAlchemy 2.0 (async).

The deciding factor is operational simplicity for a PoC: zero server
infrastructure, a self-contained database file that can be seeded once
and committed, and a one-command startup (`uv run uvicorn main:app`).
The async driver (`aiosqlite`) keeps the stack consistent with the
rest of the async I/O patterns, and SQLAlchemy abstracts enough of the
engine differences that migrating to PostgreSQL later would require
minimal changes to the application code.

## Consequences

**Positive:**
- No external service dependency — the application runs with a single
  command and no Docker Compose required for development.
- The pre-seeded database file ships with the repository, making the
  project immediately runnable with real data.
- SQLAlchemy 2.0 abstracts most engine-specific behavior; a future
  migration to PostgreSQL is feasible with driver and connection string
  changes only.

**Negative:**
- SQLite does not support concurrent writes. This is acceptable for a
  single-instance PoC but rules out horizontal scaling without a
  database change.
- Some PostgreSQL features (e.g. `RETURNING`, advisory locks, full-text
  search) are unavailable or behave differently.
- The committed database file can accumulate stale data if seed scripts
  are updated but the file is not regenerated manually.

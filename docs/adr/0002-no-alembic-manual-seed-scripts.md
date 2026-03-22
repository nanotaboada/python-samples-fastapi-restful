# ADR-0002: No Alembic — Manual Seed Scripts

Date: 2026-03-21

## Status

Accepted. Migration to Alembic is under consideration — tracked in
issue #2.

## Context

SQLAlchemy projects typically use Alembic to manage schema migrations:
versioned migration scripts, upgrade/downgrade paths, and a migration
history table. The alternatives considered were:

- **Alembic** — the standard SQLAlchemy migration tool; provides
  versioned, reversible migrations and is well-supported in production.
- **Manual seed scripts** — standalone Python scripts in `tools/` that
  create the schema and populate data directly using SQLAlchemy models;
  no migration history, no upgrade/downgrade concept.
- **No seeding** — start from an empty database and rely on the API to
  create all data; unsuitable since the project ships a fixed dataset
  (Argentina 2022 squad).

The project uses a fixed, pre-seeded SQLite database file
(`storage/players-sqlite3.db`) committed to the repository. Schema
evolution has been infrequent and handled by regenerating the file
manually from updated seed scripts.

## Decision

We will use standalone seed scripts in `tools/` instead of Alembic.

For a PoC with a stable schema and a single committed database file,
Alembic adds tooling overhead (initialization, migration directory,
`env.py` configuration) without meaningful benefit. The seed scripts
(`tools/seed_001_starting_eleven.py`, `tools/seed_002_substitutes.py`)
are self-contained and produce a deterministic output using UUID v5
for stable, reproducible primary keys.

## Consequences

**Positive:**
- No Alembic dependency or configuration; simpler project setup.
- Seed scripts are plain Python, easy to read and modify.
- Deterministic UUID v5 keys mean the seeded database is identical
  across environments and safe to reference in tests.

**Negative:**
- No migration history. Schema changes require manually updating the
  database file and rerunning seed scripts; there is no upgrade path.
- Not suitable for a production deployment where data must be preserved
  across schema changes.
- As schema complexity grows, the absence of migration tooling becomes
  increasingly costly. Issue #2 tracks the future adoption of Alembic.

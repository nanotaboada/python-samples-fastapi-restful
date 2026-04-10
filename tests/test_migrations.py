"""
Integration tests for Alembic migration downgrade paths.

These tests exercise the downgrade() functions in each migration version,
verifying that each step removes exactly the rows it seeded and leaves the
rest of the database intact.

Tests run after test_main.py (alphabetical order). Each test downgrades one
or more steps, asserts the expected state, then restores to head before the
next test, ensuring the shared SQLite database remains consistent for any
subsequent test runs.

These tests are SQLite-only: they open the database file directly via
sqlite3.connect() to inspect raw state, which is not possible with PostgreSQL.
"""

import sqlite3

import pytest
from alembic import command

from databases.player_database import DATABASE_URL
from tests.conftest import ALEMBIC_CONFIG

pytestmark = pytest.mark.skipif(
    not DATABASE_URL.startswith("sqlite"),
    reason="Migration downgrade tests require SQLite",
)

DB_PATH = DATABASE_URL.replace("sqlite+aiosqlite:///", "")


def test_migration_downgrade_003_removes_substitutes_only():
    """Downgrade 003→002 removes the 15 seeded substitutes, leaves Starting XI."""
    command.downgrade(ALEMBIC_CONFIG, "-1")

    conn = sqlite3.connect(DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    subs = conn.execute("SELECT COUNT(*) FROM players WHERE starting11=0").fetchone()[0]
    conn.close()

    assert total == 11
    assert subs == 0

    command.upgrade(ALEMBIC_CONFIG, "head")


def test_migration_downgrade_002_removes_starting11_only():
    """Downgrade 002→001 removes the 11 seeded Starting XI, leaves table empty."""
    command.downgrade(ALEMBIC_CONFIG, "-2")

    conn = sqlite3.connect(DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    conn.close()

    assert total == 0

    command.upgrade(ALEMBIC_CONFIG, "head")


def test_migration_downgrade_001_drops_players_table():
    """Downgrade 001→base drops the players table entirely."""
    command.downgrade(ALEMBIC_CONFIG, "base")

    conn = sqlite3.connect(DB_PATH)
    table = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='players'"
    ).fetchone()
    conn.close()

    assert table is None

    command.upgrade(ALEMBIC_CONFIG, "head")

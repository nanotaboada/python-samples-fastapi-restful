"""
Integration tests for Alembic migration downgrade paths.

These tests exercise the downgrade() functions in each migration version,
verifying that each step removes exactly the rows it seeded and leaves the
rest of the database intact.

Tests run after test_main.py (alphabetical order). Each test downgrades one
or more steps, asserts the expected state, then restores to head before the
next test, ensuring the shared SQLite database remains consistent for any
subsequent test runs.
"""

import os
import sqlite3

from alembic import command
from alembic.config import Config

_DB_PATH = os.getenv("STORAGE_PATH", "./players-sqlite3.db")
_ALEMBIC_CFG = Config("alembic.ini")


def test_migration_downgrade_003_removes_substitutes_only():
    """Downgrade 003→002 removes the 15 seeded substitutes, leaves Starting XI."""
    command.downgrade(_ALEMBIC_CFG, "-1")

    conn = sqlite3.connect(_DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    subs = conn.execute("SELECT COUNT(*) FROM players WHERE starting11=0").fetchone()[0]
    conn.close()

    command.upgrade(_ALEMBIC_CFG, "head")

    assert total == 11
    assert subs == 0


def test_migration_downgrade_002_removes_starting11_only():
    """Downgrade 002→001 removes the 11 seeded Starting XI, leaves table empty."""
    command.downgrade(_ALEMBIC_CFG, "-2")

    conn = sqlite3.connect(_DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    conn.close()

    command.upgrade(_ALEMBIC_CFG, "head")

    assert total == 0


def test_migration_downgrade_001_drops_players_table():
    """Downgrade 001→base drops the players table entirely."""
    command.downgrade(_ALEMBIC_CFG, "base")

    conn = sqlite3.connect(_DB_PATH)
    table = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='players'"
    ).fetchone()
    conn.close()

    command.upgrade(_ALEMBIC_CFG, "head")

    assert table is None

"""
Seed 002 – Substitutes

Seeds the 14 substitute players from the 2022 FIFA World Cup squad of the
Argentina national football team into an already-seeded `players` table
(UUID primary key, created by Seed 001).

Usage:
    python tools/seed_002_substitutes.py [--db-path PATH]

Flags:
    --db-path   Path to the SQLite database file.
                Defaults to ./storage/players-sqlite3.db

Idempotency:
    If all 14 substitute UUIDs are already present the script exits without
    making any changes.

Prerequisite:
    Seed 001 must have been executed before running this script.
    The `players` table must already exist with a TEXT (UUID) primary key.
"""

import argparse
import logging
import sqlite3
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# UUID v5 (namespace-based, deterministic) values for each substitute player.
# See seed_001_starting_eleven.py for the rationale behind using UUID v5
# in migrations versus UUID v4 for API-created records.
# ---------------------------------------------------------------------------
SUBSTITUTES = [
    {
        "id": "52524d6e-10dc-5261-aa36-8b2efcbaa5f0",
        "firstName": "Franco",
        "middleName": "Daniel",
        "lastName": "Armani",
        "dateOfBirth": "1986-10-16T00:00:00.000Z",
        "squadNumber": 1,
        "position": "Goalkeeper",
        "abbrPosition": "GK",
        "team": "River Plate",
        "league": "Copa de la Liga",
        "starting11": 0,
    },
    {
        "id": "91c274f2-9a0d-5ce6-ac3d-7529f452df21",
        "firstName": "Gerónimo",
        "middleName": None,
        "lastName": "Rulli",
        "dateOfBirth": "1992-05-20T00:00:00.000Z",
        "squadNumber": 12,
        "position": "Goalkeeper",
        "abbrPosition": "GK",
        "team": "Ajax Amsterdam",
        "league": "Eredivisie",
        "starting11": 0,
    },
    {
        "id": "0ff1e264-520d-543a-87dd-181a491e667e",
        "firstName": "Juan",
        "middleName": "Marcos",
        "lastName": "Foyth",
        "dateOfBirth": "1998-01-12T00:00:00.000Z",
        "squadNumber": 2,
        "position": "Right-Back",
        "abbrPosition": "RB",
        "team": "Villarreal",
        "league": "La Liga",
        "starting11": 0,
    },
    {
        "id": "23986425-d3a5-5e13-8bab-299745777a8d",
        "firstName": "Gonzalo",
        "middleName": "Ariel",
        "lastName": "Montiel",
        "dateOfBirth": "1997-01-01T00:00:00.000Z",
        "squadNumber": 4,
        "position": "Right-Back",
        "abbrPosition": "RB",
        "team": "Nottingham Forest",
        "league": "Premier League",
        "starting11": 0,
    },
    {
        "id": "c15b38c9-9a3e-543c-a703-dd742f25b4d5",
        "firstName": "Germán",
        "middleName": "Alejo",
        "lastName": "Pezzella",
        "dateOfBirth": "1991-06-27T00:00:00.000Z",
        "squadNumber": 6,
        "position": "Centre-Back",
        "abbrPosition": "CB",
        "team": "Real Betis Balompié",
        "league": "La Liga",
        "starting11": 0,
    },
    {
        "id": "db680066-c83d-5ed7-89a4-1d79466ea62d",
        "firstName": "Marcos",
        "middleName": "Javier",
        "lastName": "Acuña",
        "dateOfBirth": "1991-10-28T00:00:00.000Z",
        "squadNumber": 8,
        "position": "Left-Back",
        "abbrPosition": "LB",
        "team": "Sevilla FC",
        "league": "La Liga",
        "starting11": 0,
    },
    {
        "id": "cadb7952-2bba-5609-88d4-8e47ec4e7920",
        "firstName": "Lisandro",
        "middleName": None,
        "lastName": "Martínez",
        "dateOfBirth": "1998-01-18T00:00:00.000Z",
        "squadNumber": 25,
        "position": "Centre-Back",
        "abbrPosition": "CB",
        "team": "Manchester United",
        "league": "Premier League",
        "starting11": 0,
    },
    {
        "id": "35140057-a2a4-5adb-a500-46f8ed8b66a9",
        "firstName": "Leandro",
        "middleName": "Daniel",
        "lastName": "Paredes",
        "dateOfBirth": "1994-06-29T00:00:00.000Z",
        "squadNumber": 5,
        "position": "Defensive Midfield",
        "abbrPosition": "DM",
        "team": "AS Roma",
        "league": "Serie A",
        "starting11": 0,
    },
    {
        "id": "66e549b7-01e2-5d07-98d5-430f74d8d3b2",
        "firstName": "Exequiel",
        "middleName": "Alejandro",
        "lastName": "Palacios",
        "dateOfBirth": "1998-10-05T00:00:00.000Z",
        "squadNumber": 14,
        "position": "Central Midfield",
        "abbrPosition": "CM",
        "team": "Bayer 04 Leverkusen",
        "league": "Bundesliga",
        "starting11": 0,
    },
    {
        "id": "292c8e99-2378-55aa-83d8-350e0ac3f1cc",
        "firstName": "Alejandro",
        "middleName": "Darío",
        "lastName": "Gómez",
        "dateOfBirth": "1988-02-15T00:00:00.000Z",
        "squadNumber": 17,
        "position": "Left Winger",
        "abbrPosition": "LW",
        "team": "AC Monza",
        "league": "Serie A",
        "starting11": 0,
    },
    {
        "id": "0e3b230a-0509-55d8-96a0-9875f387a2be",
        "firstName": "Guido",
        "middleName": None,
        "lastName": "Rodríguez",
        "dateOfBirth": "1994-04-12T00:00:00.000Z",
        "squadNumber": 18,
        "position": "Defensive Midfield",
        "abbrPosition": "DM",
        "team": "Real Betis Balompié",
        "league": "La Liga",
        "starting11": 0,
    },
    {
        "id": "4c507660-a83b-55c0-9b2b-83eccb07723d",
        "firstName": "Ángel",
        "middleName": "Martín",
        "lastName": "Correa",
        "dateOfBirth": "1995-03-09T00:00:00.000Z",
        "squadNumber": 15,
        "position": "Right Winger",
        "abbrPosition": "RW",
        "team": "Atlético Madrid",
        "league": "La Liga",
        "starting11": 0,
    },
    {
        "id": "c2708a8b-120a-56f5-a30d-990048af87cc",
        "firstName": "Paulo",
        "middleName": "Exequiel",
        "lastName": "Dybala",
        "dateOfBirth": "1993-11-15T00:00:00.000Z",
        "squadNumber": 21,
        "position": "Second Striker",
        "abbrPosition": "SS",
        "team": "AS Roma",
        "league": "Serie A",
        "starting11": 0,
    },
    {
        "id": "e7263999-68b6-5a23-b530-af25b7efd632",
        "firstName": "Lautaro",
        "middleName": "Javier",
        "lastName": "Martínez",
        "dateOfBirth": "1997-08-22T00:00:00.000Z",
        "squadNumber": 22,
        "position": "Centre-Forward",
        "abbrPosition": "CF",
        "team": "Inter Milan",
        "league": "Serie A",
        "starting11": 0,
    },
]

INSERT_SQL = """
INSERT OR IGNORE INTO players
    (id, firstName, middleName, lastName, dateOfBirth,
     squadNumber, position, abbrPosition, team, league, starting11)
VALUES
    (:id, :firstName, :middleName, :lastName, :dateOfBirth,
     :squadNumber, :position, :abbrPosition, :team, :league, :starting11)
"""


def _table_exists(conn: sqlite3.Connection) -> bool:
    """Return True when the `players` table is present."""
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='players'"
    )
    return cursor.fetchone() is not None


def _already_migrated(conn: sqlite3.Connection) -> bool:
    """Return True when all 14 substitute UUIDs are already in the table."""
    uuids = [p["id"] for p in SUBSTITUTES]
    placeholders = ",".join("?" * len(uuids))
    cursor = conn.execute(
        f"SELECT COUNT(*) FROM players WHERE id IN ({placeholders})", uuids
    )
    return cursor.fetchone()[0] == len(uuids)


def run(db_path: Path) -> None:
    """Execute migration 002."""
    if not db_path.exists():
        logger.error("Database not found: %s", db_path)
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    try:
        if not _table_exists(conn):
            logger.error(
                "The 'players' table does not exist. "
                "Run seed_001_starting_eleven.py first."
            )
            sys.exit(1)

        if _already_migrated(conn):
            logger.info(
                "Migration 002 already applied - all substitute UUIDs present. "
                "Skipping."
            )
            return

        logger.info("Inserting %d substitute players.", len(SUBSTITUTES))
        conn.executemany(INSERT_SQL, SUBSTITUTES)
        conn.commit()

        logger.info("Migration 002 - Substitutes completed successfully.")

    except sqlite3.Error as exc:
        conn.rollback()
        logger.exception("Migration failed: %s", exc)
        sys.exit(1)
    finally:
        conn.close()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Migration 002 - seed substitute players with UUID PKs."
    )
    parser.add_argument(
        "--db-path",
        default="./storage/players-sqlite3.db",
        help="Path to the SQLite database file (default: ./storage/players-sqlite3.db)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    run(Path(args.db_path))

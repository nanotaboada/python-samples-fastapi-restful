"""
Seed 002 – Substitutes

Seeds the 15 substitute players from the 2022 FIFA World Cup squad of the
Argentina national football team into an already-seeded `players` table
(UUID primary key, created by Seed 001).

Usage:
    python tools/seed_002_substitutes.py [--db-path PATH]

Flags:
    --db-path   Path to the SQLite database file.
                Defaults to ./storage/players-sqlite3.db

Idempotency:
    If all 15 substitute UUIDs are already present the script exits without
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
        "id": "5a9cd988-95e6-54c1-bc34-9aa08acca8d0",
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
        "id": "c62f2ac1-41e8-5d34-b073-2ba0913d0e31",
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
        "id": "5fdb10e8-38c0-5084-9a3f-b369a960b9c2",
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
        "id": "bbd441f7-fcfb-5834-8468-2a9004b64c8c",
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
        "id": "d8bfea25-f189-5d5e-b3a5-ed89329b9f7c",
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
        "id": "dca343a8-12e5-53d6-89a8-916b120a5ee4",
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
        "id": "98306555-a466-5d18-804e-dc82175e697b",
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
        "id": "9d140400-196f-55d8-86e1-e0b96a375c83",
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
        "id": "d3b0e8e8-2c34-531a-b608-b24fed0ef986",
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
        "id": "7cc8d527-56a2-58bd-9528-2618fc139d30",
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
        "id": "191c82af-0c51-526a-b903-c3600b61b506",
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
        "id": "b1306b7b-a3a4-5f7c-90fd-dd5bdbed57ba",
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
        "id": "ecec27e8-487b-5622-b116-0855020477ed",
        "firstName": "Thiago",
        "middleName": "Ezequiel",
        "lastName": "Almada",
        "dateOfBirth": "2001-04-26T00:00:00.000Z",
        "squadNumber": 16,
        "position": "Attacking Midfield",
        "abbrPosition": "AM",
        "team": "Atlanta United FC",
        "league": "Major League Soccer",
        "starting11": 0,
    },
    {
        "id": "7941cd7c-4df1-5952-97e8-1e7f5d08e8aa",
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
        "id": "79c96f29-c59f-5f98-96b8-3a5946246624",
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
    """Return True when all 15 substitute UUIDs are already in the table."""
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

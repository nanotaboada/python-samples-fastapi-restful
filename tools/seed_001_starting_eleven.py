"""
Seed 001 – Starting Eleven

Recreates the `players` table using a UUID primary key (stored as TEXT in SQLite)
and seeds the 11 starting-eleven players from the 2022 FIFA World Cup squad of the
Argentina national football team.

Usage:
    python tools/seed_001_starting_eleven.py [--db-path PATH]

Flags:
    --db-path   Path to the SQLite database file.
                Defaults to ./storage/players-sqlite3.db

Idempotency:
    If all 11 starting-eleven UUIDs are already present the script exits without
    making any changes.

Backup:
    A timestamped copy of the original database is written to the same directory
    before any destructive operation (e.g. players-sqlite3.db.bak.20260219T120000).
"""

import argparse
import logging
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# UUID v5 (namespace-based, deterministic) values for each starting-eleven
# player. Using UUID v5 guarantees that the same player always gets the same
# ID regardless of when or where the migration runs, which makes these values
# safe to hardcode in test fixtures. Records created later through the API
# (POST) use UUID v4 (randomly generated) instead — there is no natural stable
# key to derive a deterministic UUID from for user-supplied data.
# ---------------------------------------------------------------------------
STARTING_ELEVEN = [
    {
        "id": "01772c59-43f0-5d85-b913-c78e4e281452",
        "firstName": "Damián",
        "middleName": "Emiliano",
        "lastName": "Martínez",
        "dateOfBirth": "1992-09-02T00:00:00.000Z",
        "squadNumber": 23,
        "position": "Goalkeeper",
        "abbrPosition": "GK",
        "team": "Aston Villa FC",
        "league": "Premier League",
        "starting11": 1,
    },
    {
        "id": "da31293b-4c7e-5e0f-a168-469ee29ecbc4",
        "firstName": "Nahuel",
        "middleName": None,
        "lastName": "Molina",
        "dateOfBirth": "1998-04-06T00:00:00.000Z",
        "squadNumber": 26,
        "position": "Right-Back",
        "abbrPosition": "RB",
        "team": "Atlético Madrid",
        "league": "La Liga",
        "starting11": 1,
    },
    {
        "id": "c096c69e-762b-5281-9290-bb9c167a24a0",
        "firstName": "Cristian",
        "middleName": "Gabriel",
        "lastName": "Romero",
        "dateOfBirth": "1998-04-27T00:00:00.000Z",
        "squadNumber": 13,
        "position": "Centre-Back",
        "abbrPosition": "CB",
        "team": "Tottenham Hotspur",
        "league": "Premier League",
        "starting11": 1,
    },
    {
        "id": "d5f7dd7a-1dcb-5960-ba27-e34865b63358",
        "firstName": "Nicolás",
        "middleName": "Hernán Gonzalo",
        "lastName": "Otamendi",
        "dateOfBirth": "1988-02-12T00:00:00.000Z",
        "squadNumber": 19,
        "position": "Centre-Back",
        "abbrPosition": "CB",
        "team": "SL Benfica",
        "league": "Liga Portugal",
        "starting11": 1,
    },
    {
        "id": "2f6f90a0-9b9d-5023-96d2-a2aaf03143a6",
        "firstName": "Nicolás",
        "middleName": "Alejandro",
        "lastName": "Tagliafico",
        "dateOfBirth": "1992-08-31T00:00:00.000Z",
        "squadNumber": 3,
        "position": "Left-Back",
        "abbrPosition": "LB",
        "team": "Olympique Lyon",
        "league": "Ligue 1",
        "starting11": 1,
    },
    {
        "id": "b5b46e79-929e-5ed2-949d-0d167109c022",
        "firstName": "Ángel",
        "middleName": "Fabián",
        "lastName": "Di María",
        "dateOfBirth": "1988-02-14T00:00:00.000Z",
        "squadNumber": 11,
        "position": "Right Winger",
        "abbrPosition": "RW",
        "team": "SL Benfica",
        "league": "Liga Portugal",
        "starting11": 1,
    },
    {
        "id": "0293b282-1da8-562e-998e-83849b417a42",
        "firstName": "Rodrigo",
        "middleName": "Javier",
        "lastName": "de Paul",
        "dateOfBirth": "1994-05-24T00:00:00.000Z",
        "squadNumber": 7,
        "position": "Central Midfield",
        "abbrPosition": "CM",
        "team": "Atlético Madrid",
        "league": "La Liga",
        "starting11": 1,
    },
    {
        "id": "d3ba552a-dac3-588a-b961-1ea7224017fd",
        "firstName": "Enzo",
        "middleName": "Jeremías",
        "lastName": "Fernández",
        "dateOfBirth": "2001-01-17T00:00:00.000Z",
        "squadNumber": 24,
        "position": "Central Midfield",
        "abbrPosition": "CM",
        "team": "SL Benfica",
        "league": "Liga Portugal",
        "starting11": 1,
    },
    {
        "id": "9613cae9-16ab-5b54-937e-3135123b9e0d",
        "firstName": "Alexis",
        "middleName": None,
        "lastName": "Mac Allister",
        "dateOfBirth": "1998-12-24T00:00:00.000Z",
        "squadNumber": 20,
        "position": "Central Midfield",
        "abbrPosition": "CM",
        "team": "Brighton & Hove Albion",
        "league": "Premier League",
        "starting11": 1,
    },
    {
        "id": "acc433bf-d505-51fe-831e-45eb44c4d43c",
        "firstName": "Lionel",
        "middleName": "Andrés",
        "lastName": "Messi",
        "dateOfBirth": "1987-06-24T00:00:00.000Z",
        "squadNumber": 10,
        "position": "Right Winger",
        "abbrPosition": "RW",
        "team": "Paris Saint-Germain",
        "league": "Ligue 1",
        "starting11": 1,
    },
    {
        "id": "38bae91d-8519-55a2-b30a-b9fe38849bfb",
        "firstName": "Julián",
        "middleName": None,
        "lastName": "Álvarez",
        "dateOfBirth": "2000-01-31T00:00:00.000Z",
        "squadNumber": 9,
        "position": "Centre-Forward",
        "abbrPosition": "CF",
        "team": "Manchester City",
        "league": "Premier League",
        "starting11": 1,
    },
]

CREATE_TABLE_SQL = """
CREATE TABLE players (
    id          TEXT PRIMARY KEY NOT NULL,
    firstName   TEXT NOT NULL,
    middleName  TEXT,
    lastName    TEXT NOT NULL,
    dateOfBirth TEXT,
    squadNumber INTEGER NOT NULL UNIQUE,
    position    TEXT NOT NULL,
    abbrPosition TEXT,
    team        TEXT,
    league      TEXT,
    starting11  INTEGER
)
"""

INSERT_SQL = """
INSERT OR IGNORE INTO players
    (id, firstName, middleName, lastName, dateOfBirth,
     squadNumber, position, abbrPosition, team, league, starting11)
VALUES
    (:id, :firstName, :middleName, :lastName, :dateOfBirth,
     :squadNumber, :position, :abbrPosition, :team, :league, :starting11)
"""


def _id_column_type(conn: sqlite3.Connection) -> str:
    """Return the SQLite type of the 'id' column, or '' if the table is absent."""
    cursor = conn.execute("PRAGMA table_info(players)")
    for row in cursor.fetchall():
        if row[1] == "id":
            return row[2].upper()
    return ""


def _already_migrated(conn: sqlite3.Connection) -> bool:
    """Return True when all 11 starting-eleven UUIDs are already in the table."""
    uuids = [p["id"] for p in STARTING_ELEVEN]
    placeholders = ",".join("?" * len(uuids))
    cursor = conn.execute(
        f"SELECT COUNT(*) FROM players WHERE id IN ({placeholders})", uuids
    )
    return cursor.fetchone()[0] == len(uuids)


def _backup(db_path: Path) -> None:
    """Write a timestamped backup of the database file."""
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    backup_path = db_path.with_suffix(f".db.bak.{stamp}")
    shutil.copy2(db_path, backup_path)
    logger.info("Backup created: %s", backup_path)


def run(db_path: Path) -> None:
    """Execute migration 001."""
    if not db_path.exists():
        logger.error("Database not found: %s", db_path)
        sys.exit(1)

    conn = sqlite3.connect(db_path)

    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")

        id_type = _id_column_type(conn)

        if id_type == "TEXT" and _already_migrated(conn):
            logger.info(
                "Migration 001 already applied – all starting-eleven UUIDs present. "
                "Skipping."
            )
            return

        _backup(db_path)

        if id_type != "":
            # Drop the old table (INTEGER or partially migrated schema)
            logger.info("Dropping existing 'players' table (id type: %s).", id_type)
            conn.execute("DROP TABLE IF EXISTS players")

        logger.info("Creating 'players' table with UUID primary key.")
        conn.execute(CREATE_TABLE_SQL)

        logger.info("Inserting %d starting-eleven players.", len(STARTING_ELEVEN))
        conn.executemany(INSERT_SQL, STARTING_ELEVEN)
        conn.commit()

        logger.info("Migration 001 – Starting Eleven completed successfully.")

    except sqlite3.Error as exc:
        conn.rollback()
        logger.exception("Migration failed: %s", exc)
        sys.exit(1)
    finally:
        conn.close()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Migration 001 – seed starting-eleven players with UUID PKs."
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

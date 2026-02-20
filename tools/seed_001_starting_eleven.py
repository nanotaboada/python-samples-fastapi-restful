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
        "id": "b04965e6-a9bb-591f-8f8a-1adcb2c8dc39",
        "firstName": "Emiliano",
        "middleName": None,
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
        "id": "4b166dbe-d99d-5091-abdd-95b83330ed3a",
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
        "id": "98123fde-012f-5ff3-8b50-881449dac91a",
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
        "id": "6ed955c6-506a-5343-9be4-2c0afae02eef",
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
        "id": "c8691da2-158a-5ed6-8537-0e6f140801f2",
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
        "id": "a6c4fc8f-6950-51de-a9ae-2c519c465071",
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
        "id": "a9f96b98-dd44-5216-ab0d-dbfc6b262edf",
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
        "id": "e99caacd-6c45-5906-bd9f-b79e62f25963",
        "firstName": "Enzo",
        "middleName": "Jeremías",
        "lastName": "Fernández",
        "dateOfBirth": "2001-01-17T00:00:00.000Z",
        "squadNumber": 24,
        "position": "Central Midfield",
        "abbrPosition": "CM",
        "team": "Chelsea FC",
        "league": "Premier League",
        "starting11": 1,
    },
    {
        "id": "e4d80b30-151e-51b5-9f4f-18a3b82718e6",
        "firstName": "Alexis",
        "middleName": None,
        "lastName": "Mac Allister",
        "dateOfBirth": "1998-12-24T00:00:00.000Z",
        "squadNumber": 20,
        "position": "Central Midfield",
        "abbrPosition": "CM",
        "team": "Liverpool FC",
        "league": "Premier League",
        "starting11": 1,
    },
    {
        "id": "0159d6c7-973f-5e7a-a9a0-d195d0ea6fe2",
        "firstName": "Lionel",
        "middleName": "Andrés",
        "lastName": "Messi",
        "dateOfBirth": "1987-06-24T00:00:00.000Z",
        "squadNumber": 10,
        "position": "Right Winger",
        "abbrPosition": "RW",
        "team": "Inter Miami CF",
        "league": "Major League Soccer",
        "starting11": 1,
    },
    {
        "id": "7fef88f7-411d-5669-b42d-bf5fc7f9b58b",
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
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    try:
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

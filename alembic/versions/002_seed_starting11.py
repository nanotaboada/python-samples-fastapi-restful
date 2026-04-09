"""Seed Starting XI players

Seeds the 11 Starting XI players from the 2022 FIFA World Cup squad of the
Argentina national football team. Uses deterministic UUID v5 values so that
IDs are stable across environments.

Revision ID: 002
Revises: 001
Create Date: 2026-04-09

"""

from typing import Sequence, Union

from alembic import op

revision: str = "002"
down_revision: Union[str, Sequence[str], None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# UUID v5 (deterministic) values — stable across environments.
# See schemas/player_schema.py for the rationale.
_STARTING_ELEVEN_SQL = """
INSERT INTO players
    (id, firstName, middleName, lastName, dateOfBirth,
     squadNumber, position, abbrPosition, team, league, starting11)
VALUES
    ('01772c59-43f0-5d85-b913-c78e4e281452', 'Damián', 'Emiliano', 'Martínez',
     '1992-09-02T00:00:00.000Z', 23, 'Goalkeeper', 'GK', 'Aston Villa FC',
     'Premier League', 1),
    ('da31293b-4c7e-5e0f-a168-469ee29ecbc4', 'Nahuel', NULL, 'Molina',
     '1998-04-06T00:00:00.000Z', 26, 'Right-Back', 'RB', 'Atlético Madrid',
     'La Liga', 1),
    ('c096c69e-762b-5281-9290-bb9c167a24a0', 'Cristian', 'Gabriel', 'Romero',
     '1998-04-27T00:00:00.000Z', 13, 'Centre-Back', 'CB', 'Tottenham Hotspur',
     'Premier League', 1),
    ('d5f7dd7a-1dcb-5960-ba27-e34865b63358', 'Nicolás', 'Hernán Gonzalo', 'Otamendi',
     '1988-02-12T00:00:00.000Z', 19, 'Centre-Back', 'CB', 'SL Benfica',
     'Liga Portugal', 1),
    ('2f6f90a0-9b9d-5023-96d2-a2aaf03143a6', 'Nicolás', 'Alejandro', 'Tagliafico',
     '1992-08-31T00:00:00.000Z', 3, 'Left-Back', 'LB', 'Olympique Lyon',
     'Ligue 1', 1),
    ('b5b46e79-929e-5ed2-949d-0d167109c022', 'Ángel', 'Fabián', 'Di María',
     '1988-02-14T00:00:00.000Z', 11, 'Right Winger', 'RW', 'SL Benfica',
     'Liga Portugal', 1),
    ('0293b282-1da8-562e-998e-83849b417a42', 'Rodrigo', 'Javier', 'de Paul',
     '1994-05-24T00:00:00.000Z', 7, 'Central Midfield', 'CM', 'Atlético Madrid',
     'La Liga', 1),
    ('d3ba552a-dac3-588a-b961-1ea7224017fd', 'Enzo', 'Jeremías', 'Fernández',
     '2001-01-17T00:00:00.000Z', 24, 'Central Midfield', 'CM', 'SL Benfica',
     'Liga Portugal', 1),
    ('9613cae9-16ab-5b54-937e-3135123b9e0d', 'Alexis', NULL, 'Mac Allister',
     '1998-12-24T00:00:00.000Z', 20, 'Central Midfield', 'CM',
     'Brighton & Hove Albion', 'Premier League', 1),
    ('acc433bf-d505-51fe-831e-45eb44c4d43c', 'Lionel', 'Andrés', 'Messi',
     '1987-06-24T00:00:00.000Z', 10, 'Right Winger', 'RW', 'Paris Saint-Germain',
     'Ligue 1', 1),
    ('38bae91d-8519-55a2-b30a-b9fe38849bfb', 'Julián', NULL, 'Álvarez',
     '2000-01-31T00:00:00.000Z', 9, 'Centre-Forward', 'CF', 'Manchester City',
     'Premier League', 1)
"""

_SEEDED_IDS = (
    "'01772c59-43f0-5d85-b913-c78e4e281452'",
    "'da31293b-4c7e-5e0f-a168-469ee29ecbc4'",
    "'c096c69e-762b-5281-9290-bb9c167a24a0'",
    "'d5f7dd7a-1dcb-5960-ba27-e34865b63358'",
    "'2f6f90a0-9b9d-5023-96d2-a2aaf03143a6'",
    "'b5b46e79-929e-5ed2-949d-0d167109c022'",
    "'0293b282-1da8-562e-998e-83849b417a42'",
    "'d3ba552a-dac3-588a-b961-1ea7224017fd'",
    "'9613cae9-16ab-5b54-937e-3135123b9e0d'",
    "'acc433bf-d505-51fe-831e-45eb44c4d43c'",
    "'38bae91d-8519-55a2-b30a-b9fe38849bfb'",
)


def upgrade() -> None:
    op.execute(_STARTING_ELEVEN_SQL)


def downgrade() -> None:
    ids = ", ".join(_SEEDED_IDS)
    op.execute(f"DELETE FROM players WHERE id IN ({ids})")

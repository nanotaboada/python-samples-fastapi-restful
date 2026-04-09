"""Seed Substitute players

Seeds the 15 Substitute players from the 2022 FIFA World Cup squad of the
Argentina national football team. Uses deterministic UUID v5 values so that
IDs are stable across environments.

Rolling back this migration removes only substitutes, leaving Starting XI
(migration 002) intact.

Revision ID: 003
Revises: 002
Create Date: 2026-04-09

"""

from typing import Sequence, Union

from alembic import op

revision: str = "003"
down_revision: Union[str, Sequence[str], None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# UUID v5 (deterministic) values — stable across environments.
# See schemas/player_schema.py for the rationale.
_SUBSTITUTES_SQL = """
INSERT INTO players
    (id, firstName, middleName, lastName, dateOfBirth,
     squadNumber, position, abbrPosition, team, league, starting11)
VALUES
    ('5a9cd988-95e6-54c1-bc34-9aa08acca8d0', 'Franco', 'Daniel', 'Armani',
     '1986-10-16T00:00:00.000Z', 1, 'Goalkeeper', 'GK', 'River Plate',
     'Copa de la Liga', 0),
    ('c62f2ac1-41e8-5d34-b073-2ba0913d0e31', 'Gerónimo', NULL, 'Rulli',
     '1992-05-20T00:00:00.000Z', 12, 'Goalkeeper', 'GK', 'Ajax Amsterdam',
     'Eredivisie', 0),
    ('5fdb10e8-38c0-5084-9a3f-b369a960b9c2', 'Juan', 'Marcos', 'Foyth',
     '1998-01-12T00:00:00.000Z', 2, 'Right-Back', 'RB', 'Villarreal',
     'La Liga', 0),
    ('bbd441f7-fcfb-5834-8468-2a9004b64c8c', 'Gonzalo', 'Ariel', 'Montiel',
     '1997-01-01T00:00:00.000Z', 4, 'Right-Back', 'RB', 'Nottingham Forest',
     'Premier League', 0),
    ('d8bfea25-f189-5d5e-b3a5-ed89329b9f7c', 'Germán', 'Alejo', 'Pezzella',
     '1991-06-27T00:00:00.000Z', 6, 'Centre-Back', 'CB', 'Real Betis Balompié',
     'La Liga', 0),
    ('dca343a8-12e5-53d6-89a8-916b120a5ee4', 'Marcos', 'Javier', 'Acuña',
     '1991-10-28T00:00:00.000Z', 8, 'Left-Back', 'LB', 'Sevilla FC',
     'La Liga', 0),
    ('98306555-a466-5d18-804e-dc82175e697b', 'Lisandro', NULL, 'Martínez',
     '1998-01-18T00:00:00.000Z', 25, 'Centre-Back', 'CB', 'Manchester United',
     'Premier League', 0),
    ('9d140400-196f-55d8-86e1-e0b96a375c83', 'Leandro', 'Daniel', 'Paredes',
     '1994-06-29T00:00:00.000Z', 5, 'Defensive Midfield', 'DM', 'AS Roma',
     'Serie A', 0),
    ('d3b0e8e8-2c34-531a-b608-b24fed0ef986', 'Exequiel', 'Alejandro', 'Palacios',
     '1998-10-05T00:00:00.000Z', 14, 'Central Midfield', 'CM',
     'Bayer 04 Leverkusen', 'Bundesliga', 0),
    ('7cc8d527-56a2-58bd-9528-2618fc139d30', 'Alejandro', 'Darío', 'Gómez',
     '1988-02-15T00:00:00.000Z', 17, 'Left Winger', 'LW', 'AC Monza',
     'Serie A', 0),
    ('191c82af-0c51-526a-b903-c3600b61b506', 'Guido', NULL, 'Rodríguez',
     '1994-04-12T00:00:00.000Z', 18, 'Defensive Midfield', 'DM',
     'Real Betis Balompié', 'La Liga', 0),
    ('b1306b7b-a3a4-5f7c-90fd-dd5bdbed57ba', 'Ángel', 'Martín', 'Correa',
     '1995-03-09T00:00:00.000Z', 15, 'Right Winger', 'RW', 'Atlético Madrid',
     'La Liga', 0),
    ('ecec27e8-487b-5622-b116-0855020477ed', 'Thiago', 'Ezequiel', 'Almada',
     '2001-04-26T00:00:00.000Z', 16, 'Attacking Midfield', 'AM',
     'Atlanta United FC', 'Major League Soccer', 0),
    ('7941cd7c-4df1-5952-97e8-1e7f5d08e8aa', 'Paulo', 'Exequiel', 'Dybala',
     '1993-11-15T00:00:00.000Z', 21, 'Second Striker', 'SS', 'AS Roma',
     'Serie A', 0),
    ('79c96f29-c59f-5f98-96b8-3a5946246624', 'Lautaro', 'Javier', 'Martínez',
     '1997-08-22T00:00:00.000Z', 22, 'Centre-Forward', 'CF', 'Inter Milan',
     'Serie A', 0)
"""

_SEEDED_IDS = (
    "'5a9cd988-95e6-54c1-bc34-9aa08acca8d0'",
    "'c62f2ac1-41e8-5d34-b073-2ba0913d0e31'",
    "'5fdb10e8-38c0-5084-9a3f-b369a960b9c2'",
    "'bbd441f7-fcfb-5834-8468-2a9004b64c8c'",
    "'d8bfea25-f189-5d5e-b3a5-ed89329b9f7c'",
    "'dca343a8-12e5-53d6-89a8-916b120a5ee4'",
    "'98306555-a466-5d18-804e-dc82175e697b'",
    "'9d140400-196f-55d8-86e1-e0b96a375c83'",
    "'d3b0e8e8-2c34-531a-b608-b24fed0ef986'",
    "'7cc8d527-56a2-58bd-9528-2618fc139d30'",
    "'191c82af-0c51-526a-b903-c3600b61b506'",
    "'b1306b7b-a3a4-5f7c-90fd-dd5bdbed57ba'",
    "'ecec27e8-487b-5622-b116-0855020477ed'",
    "'7941cd7c-4df1-5952-97e8-1e7f5d08e8aa'",
    "'79c96f29-c59f-5f98-96b8-3a5946246624'",
)


def upgrade() -> None:
    op.execute(_SUBSTITUTES_SQL)


def downgrade() -> None:
    ids = ", ".join(_SEEDED_IDS)
    op.execute(f"DELETE FROM players WHERE id IN ({ids})")

# -------------------------------------------------------------------------------------------------
# Service
# -------------------------------------------------------------------------------------------------

from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.player_schema import Player


# https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-usage


def retrieve_all_players(orm_session: Session):
    players = orm_session.execute(
        select(Player)
    ).scalars().all()
    return players


def retrieve_player_by_id(orm_session: Session, player_id: int):
    player = orm_session.get(Player, player_id)
    return player


def retrieve_player_by_squad_number(orm_session: Session, squad_number: int):
    player = orm_session.execute(
        select(Player).where(Player.squad_number == squad_number)
    ).scalars().first()
    return player

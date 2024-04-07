# -------------------------------------------------------------------------------------------------
# Service
# -------------------------------------------------------------------------------------------------

from sqlalchemy.orm import Session
from schemas.player_schema import Player


# https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.all
def retrieve_all_players(orm_session: Session):
    return orm_session.query(Player).all()


# https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.get
def retrieve_player_by_id(orm_session: Session, player_id: int):
    return orm_session.query(Player).filter(Player.id == player_id).first()


# https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.filter
def retrieve_player_by_squad_number(orm_session: Session, squad_number: int):
    return orm_session.query(Player).filter(Player.squad_number == squad_number).first()

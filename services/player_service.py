# -------------------------------------------------------------------------------------------------
# Service
# -------------------------------------------------------------------------------------------------

from sqlalchemy.orm import Session
from schemas.player_schema import Player


# https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.all
def retrieve_all_players(db: Session):
    return db.query(Player).all()


# https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.get
def retrieve_player_by_id(db: Session, player_id: int):
    return db.query(Player).filter(Player.id == player_id).first()


# https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.filter
def retrieve_player_by_squad_number(db: Session, squad_number: int):
    return db.query(Player).filter(Player.squad_number == squad_number).first()

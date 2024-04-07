# -------------------------------------------------------------------------------------------------
# Route
# -------------------------------------------------------------------------------------------------

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path
from data.player_database import OrmSession
from sqlalchemy.orm import Session
from models.player_model import PlayerModel
from services import player_service

api_router = APIRouter()


# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
def get_orm_session():
    orm_session = OrmSession()
    try:
        yield orm_session
    finally:
        orm_session.close()

# -------------------------------------------------------------------------------------------------
# HTTP GET
# -------------------------------------------------------------------------------------------------


@api_router.get(
    "/players/",
    response_model=List[PlayerModel],
    summary="Retrieves a collection of Players"
)
def get_players(
    orm_session: Session = Depends(get_orm_session)
):
    players = player_service.retrieve_all_players(orm_session)
    return players


@api_router.get(
    "/players/{player_id}",
    response_model=PlayerModel,
    summary="Retrieves a Player by Id"
)
def get_player_by_id(
    player_id: int = Path(..., title="The Id of the Player"),
    orm_session: Session = Depends(get_orm_session)
):
    player = player_service.retrieve_player_by_id(orm_session, player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return player


@api_router.get(
    "/players/squadnumber/{squad_number}",
    response_model=PlayerModel,
    summary="Retrieves a Player by Squad Number"
)
def get_player_by_squad_number(
    squad_number: int = Path(..., title="The Squad Number of the Player"),
    orm_session: Session = Depends(get_orm_session)
):
    player = player_service.retrieve_player_by_squad_number(orm_session, squad_number)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return player

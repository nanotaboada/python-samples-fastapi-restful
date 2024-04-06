# -------------------------------------------------------------------------------------------------
# Route
# -------------------------------------------------------------------------------------------------

from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import List
from data.player_database import OrmSession
from sqlalchemy.orm import Session
from models.player_model import PlayerModel
from services import player_service

api_router = APIRouter()

# We need to have an independent database session/connection per request, use
# the same session through all the request and then close it after the request
# is finished.
# And then a new session will be created for the next request.
# Our dependency will create a new SQLAlchemy Session that will be used in a
# single request, and then close it once the request is finished.
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency


def get_db_session():
    db_session = OrmSession()
    try:
        yield db_session
    finally:
        db_session.close()

# -------------------------------------------------------------------------------------------------
# HTTP GET
# -------------------------------------------------------------------------------------------------


@api_router.get(
    "/players/",
    response_model=List[PlayerModel],
    summary="Retrieves a collection of Players"
)
def get_players(
    db_session: Session = Depends(get_db_session)
):
    players = player_service.retrieve_all_players(db_session)
    return players


@api_router.get(
    "/players/{player_id}",
    response_model=PlayerModel,
    summary="Retrieves a Player by Id"
)
def get_player_by_id(
    player_id: int = Path(..., title="The Id of the Player"),
    db_session: Session = Depends(get_db_session)
):
    player = player_service.retrieve_player_by_id(db_session, player_id)
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
    db_session: Session = Depends(get_db_session)
):
    player = player_service.retrieve_player_by_squad_number(db_session, squad_number)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return player

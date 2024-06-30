# ------------------------------------------------------------------------------
# Route
# ------------------------------------------------------------------------------

from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from data.player_database import OrmSession
from models.player_model import PlayerModel
from services import player_service
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

api_router = APIRouter()

CACHING_TIME_IN_SECONDS = 600

# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency


def get_orm_session():
    orm_session = OrmSession()
    try:
        yield orm_session
    finally:
        orm_session.close()

# POST -------------------------------------------------------------------------


@api_router.post(
    "/players/",
    status_code=status.HTTP_201_CREATED,
    summary="Creates a new Player",
)
def post(
    player_model: PlayerModel = Body(...),
    orm_session: Session = Depends(get_orm_session),
):
    player = player_service.retrieve_by_id(orm_session, player_model.id)

    if player:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    player_service.create(orm_session, player_model)

    FastAPICache.clear()

# GET --------------------------------------------------------------------------


@api_router.get(
    "/players/",
    response_model=List[PlayerModel],
    status_code=status.HTTP_200_OK,
    summary="Retrieves a collection of Players"
)
@cache(expire=CACHING_TIME_IN_SECONDS)
def get_all(
    orm_session: Session = Depends(get_orm_session)
):
    players = player_service.retrieve_all(orm_session)

    return players


@api_router.get(
    "/players/{player_id}",
    response_model=PlayerModel,
    status_code=status.HTTP_200_OK,
    summary="Retrieves a Player by its Id"
)
@cache(expire=CACHING_TIME_IN_SECONDS)
def get_by_id(
    player_id: int = Path(..., title="The Id of the Player"),
    orm_session: Session = Depends(get_orm_session)
):
    player = player_service.retrieve_by_id(orm_session, player_id)

    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return player


@api_router.get(
    "/players/squadnumber/{squad_number}",
    response_model=PlayerModel,
    status_code=status.HTTP_200_OK,
    summary="Retrieves a Player by its Squad Number"
)
@cache(expire=CACHING_TIME_IN_SECONDS)
def get_by_squad_number(
    squad_number: int = Path(..., title="The Squad Number of the Player"),
    orm_session: Session = Depends(get_orm_session)
):
    player = player_service.retrieve_by_squad_number(orm_session, squad_number)

    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return player

# PUT --------------------------------------------------------------------------


@api_router.put(
    "/players/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Updates an existing Player"
)
def put(
    player_id: int = Path(..., title="The Id of the Player"),
    player_model: PlayerModel = Body(...),
    orm_session: Session = Depends(get_orm_session),

):
    player = player_service.retrieve_by_id(orm_session, player_id)

    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    player_service.update(orm_session, player_model)

    FastAPICache.clear()

# DELETE -----------------------------------------------------------------------


@api_router.delete(
    "/players/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes an existing Player"
)
def delete(
    player_id: int = Path(..., title="The Id of the Player"),
    orm_session: Session = Depends(get_orm_session)
):
    player = player_service.retrieve_by_id(orm_session, player_id)

    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")

    player_service.delete(orm_session, player_id)

    FastAPICache.clear()

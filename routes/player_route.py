# ------------------------------------------------------------------------------
# Route
# ------------------------------------------------------------------------------

from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from data.player_database import OrmSession
from models.player_model import PlayerModel
from services import player_service

api_router = APIRouter()

CACHING_TIME_IN_SECONDS = 600

# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency


def get_orm_session():
    """
    Dependency function to yield a scoped SQLAlchemy ORM session.

    Yields:
        OrmSession: An instance of a scoped SQLAlchemy ORM session.
    """
    orm_session = OrmSession()
    try:
        yield orm_session
    finally:
        orm_session.close()

# POST -------------------------------------------------------------------------


@api_router.post(
    "/players/",
    status_code=status.HTTP_201_CREATED,
    summary="Creates a new Player"
)
def post(
    player_model: PlayerModel = Body(...),
    orm_session: Session = Depends(get_orm_session)
):
    """
    Endpoint to create a new player.

    Args:
        player_model (PlayerModel): The data model representing a Player.
        orm_session (Session): The SQLAlchemy ORM session.

    Raises:
        HTTPException: HTTP 409 Conflict error if the Player already exists.
    """
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
    """
    Endpoint to retrieve all players.

    Args:
        orm_session (Session): The SQLAlchemy ORM session.

    Returns:
        List[PlayerModel]: A list of data models representing all players.
    """
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
    player_id: int = Path(..., title="The ID of the Player"),
    orm_session: Session = Depends(get_orm_session)
):
    """
    Endpoint to retrieve a Player by its ID.

    Args:
        player_id (int): The ID of the Player to retrieve.
        orm_session (Session): The SQLAlchemy ORM session.

    Returns:
        PlayerModel: A data model representing the Player.

    Raises:
        HTTPException: Not found error if the Player with the specified ID does not exist.
    """
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
    """
    Endpoint to retrieve a Player by its Squad Number.

    Args:
        squad_number (int): The Squad Number of the Player to retrieve.
        orm_session (Session): SQLAlchemy ORM session.

    Returns:
        PlayerModel: A data model representing the Player.

    Raises:
        HTTPException: HTTP 404 Not Found error if the Player with the specified Squad Number does not exist.
    """
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
    player_id: int = Path(..., title="The ID of the Player"),
    player_model: PlayerModel = Body(...),
    orm_session: Session = Depends(get_orm_session)
):
    """
    Endpoint to entirely update an existing Player.

    Args:
        player_id (int): The ID of the Player to update.
        player_model (PlayerModel): The data model representing the Player to update.
        orm_session (Session): The SQLAlchemy ORM session.

    Raises:
        HTTPException: HTTP 404 Not Found error if the player with the specified ID does not exist.
    """
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
    player_id: int = Path(..., title="The ID of the Player"),
    orm_session: Session = Depends(get_orm_session)
):
    """
    Endpoint to delete an existing Player.

    Args:
        player_id (int): The ID of the Player to delete.
        orm_session (Session): The SQLAlchemy ORM session.

    Raises:
        HTTPException: HTTP 404 Not Found error if the Player with the specified ID does not exist.
    """
    player = player_service.retrieve_by_id(orm_session, player_id)

    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    player_service.delete(orm_session, player_id)

    FastAPICache.clear()

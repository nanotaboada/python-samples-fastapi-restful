# ------------------------------------------------------------------------------
# Route
# ------------------------------------------------------------------------------

from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from data.player_database import generate_async_session
from models.player_model import PlayerModel
from services import player_service

api_router = APIRouter()

CACHING_TIME_IN_SECONDS = 600

# POST -------------------------------------------------------------------------


@api_router.post(
    "/players/",
    status_code=status.HTTP_201_CREATED,
    summary="Creates a new Player",
    tags=["Players"]
)
async def post_async(
    player_model: PlayerModel = Body(...),
    async_session: AsyncSession = Depends(generate_async_session)
):
    """
    Endpoint to create a new player.

    Args:
        player_model (PlayerModel): The Pydantic model representing the Player to create.
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Raises:
        HTTPException: HTTP 409 Conflict error if the Player already exists.
    """
    player = await player_service.retrieve_by_id_async(async_session, player_model.id)
    if player:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    await player_service.create_async(async_session, player_model)
    await FastAPICache.clear()

# GET --------------------------------------------------------------------------


@api_router.get(
    "/players/",
    response_model=List[PlayerModel],
    status_code=status.HTTP_200_OK,
    summary="Retrieves a collection of Players",
    tags=["Players"]
)
@cache(expire=CACHING_TIME_IN_SECONDS)
async def get_all_async(
    async_session: AsyncSession = Depends(generate_async_session)
):
    """
    Endpoint to retrieve all players.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Returns:
        List[PlayerModel]: A list of Pydantic models representing all players.
    """
    players = await player_service.retrieve_all_async(async_session)
    return players


@api_router.get(
    "/players/{player_id}",
    response_model=PlayerModel,
    status_code=status.HTTP_200_OK,
    summary="Retrieves a Player by its Id",
    tags=["Players"]
)
@cache(expire=CACHING_TIME_IN_SECONDS)
async def get_by_id_async(
    player_id: int = Path(..., title="The ID of the Player"),
    async_session: AsyncSession = Depends(generate_async_session)
):
    """
    Endpoint to retrieve a Player by its ID.

    Args:
        player_id (int): The ID of the Player to retrieve.
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Returns:
        PlayerModel: The Pydantic model representing the matching Player.

    Raises:
        HTTPException: Not found error if the Player with the specified ID does not exist.
    """
    player = await player_service.retrieve_by_id_async(async_session, player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return player


@api_router.get(
    "/players/squadnumber/{squad_number}",
    response_model=PlayerModel,
    status_code=status.HTTP_200_OK,
    summary="Retrieves a Player by its Squad Number",
    tags=["Players"]
)
@cache(expire=CACHING_TIME_IN_SECONDS)
async def get_by_squad_number_async(
    squad_number: int = Path(..., title="The Squad Number of the Player"),
    async_session: AsyncSession = Depends(generate_async_session)
):
    """
    Endpoint to retrieve a Player by its Squad Number.

    Args:
        squad_number (int): The Squad Number of the Player to retrieve.
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Returns:
        PlayerModel: The Pydantic model representing the matching Player.

    Raises:
        HTTPException: HTTP 404 Not Found error if the Player with the specified Squad Number does not exist.
    """
    player = await player_service.retrieve_by_squad_number_async(async_session, squad_number)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return player

# PUT --------------------------------------------------------------------------


@api_router.put(
    "/players/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Updates an existing Player",
    tags=["Players"]
)
async def put_async(
    player_id: int = Path(..., title="The ID of the Player"),
    player_model: PlayerModel = Body(...),
    async_session: AsyncSession = Depends(generate_async_session)
):
    """
    Endpoint to entirely update an existing Player.

    Args:
        player_id (int): The ID of the Player to update.
        player_model (PlayerModel): The Pydantic model representing the Player to update.
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Raises:
        HTTPException: HTTP 404 Not Found error if the Player with the specified ID does not exist.
    """
    player = await player_service.retrieve_by_id_async(async_session, player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await player_service.update_async(async_session, player_model)
    await FastAPICache.clear()

# DELETE -----------------------------------------------------------------------


@api_router.delete(
    "/players/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes an existing Player",
    tags=["Players"]
)
async def delete_async(
    player_id: int = Path(..., title="The ID of the Player"),
    async_session: AsyncSession = Depends(generate_async_session)
):
    """
    Endpoint to delete an existing Player.

    Args:
        player_id (int): The ID of the Player to delete.
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Raises:
        HTTPException: HTTP 404 Not Found error if the Player with the specified ID does not exist.
    """
    player = await player_service.retrieve_by_id_async(async_session, player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await player_service.delete_async(async_session, player_id)
    await FastAPICache.clear()

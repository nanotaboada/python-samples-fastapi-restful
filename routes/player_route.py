"""
API routes for managing Player resources.

Provides CRUD endpoints to create, read, update, and delete Player entities.

Features:
- Caching with in-memory cache to optimize retrieval performance.
- Async database session dependency injection.
- Standard HTTP status codes and error handling.

Endpoints:
- POST /players/                          : Create a new Player.
- GET /players/                           : Retrieve all Players.
- GET /players/{player_id}                : Retrieve Player by UUID
                                            (surrogate key, internal).
- GET /players/squadnumber/{squad_number} : Retrieve Player by Squad Number
                                            (natural key, domain).
- PUT /players/{player_id}                : Update an existing Player.
- DELETE /players/{player_id}             : Delete an existing Player.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, status, Path, Response
from sqlalchemy.ext.asyncio import AsyncSession
from aiocache import SimpleMemoryCache

from databases.player_database import generate_async_session
from models.player_model import PlayerRequestModel, PlayerResponseModel
from services import player_service

api_router = APIRouter()
simple_memory_cache = SimpleMemoryCache()

CACHE_KEY = "players"
CACHE_TTL = 600  # 10 minutes

# POST -------------------------------------------------------------------------


@api_router.post(
    "/players/",
    response_model=PlayerResponseModel,
    status_code=status.HTTP_201_CREATED,
    summary="Creates a new Player",
    tags=["Players"],
)
async def post_async(
    player_model: PlayerRequestModel = Body(...),
    async_session: AsyncSession = Depends(generate_async_session),
):
    """
    Endpoint to create a new player.

    Args:
        player_model (PlayerRequestModel): The Pydantic model representing the Player
        to create.
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Returns:
        PlayerResponseModel: The created Player with its generated UUID.

    Raises:
        HTTPException: HTTP 409 Conflict error if the Player already exists.
    """
    existing = await player_service.retrieve_by_squad_number_async(
        async_session, player_model.squad_number
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    player = await player_service.create_async(async_session, player_model)
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create the Player due to a database error.",
        )
    await simple_memory_cache.clear(CACHE_KEY)
    return player


# GET --------------------------------------------------------------------------


@api_router.get(
    "/players/",
    response_model=List[PlayerResponseModel],
    status_code=status.HTTP_200_OK,
    summary="Retrieves a collection of Players",
    tags=["Players"],
)
async def get_all_async(
    response: Response, async_session: AsyncSession = Depends(generate_async_session)
):
    """
    Endpoint to retrieve all players.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Returns:
        List[PlayerResponseModel]: A list of Pydantic models representing all players.
    """
    players = await simple_memory_cache.get(CACHE_KEY)
    response.headers["X-Cache"] = "HIT"
    if not players:
        players = await player_service.retrieve_all_async(async_session)
        await simple_memory_cache.set(CACHE_KEY, players, ttl=CACHE_TTL)
        response.headers["X-Cache"] = "MISS"
    return players


@api_router.get(
    "/players/{player_id}",
    response_model=PlayerResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Retrieves a Player by its UUID",
    tags=["Players"],
)
async def get_by_id_async(
    player_id: UUID = Path(..., title="The UUID of the Player"),
    async_session: AsyncSession = Depends(generate_async_session),
):
    """
    Endpoint to retrieve a Player by its UUID.

    Args:
        player_id (UUID): The UUID of the Player to retrieve.
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Returns:
        PlayerResponseModel: The Pydantic model representing the matching Player.

    Raises:
        HTTPException: Not found error if the Player with the specified UUID does not
        exist.
    """
    player = await player_service.retrieve_by_id_async(async_session, player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return player


@api_router.get(
    "/players/squadnumber/{squad_number}",
    response_model=PlayerResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Retrieves a Player by its Squad Number",
    tags=["Players"],
)
async def get_by_squad_number_async(
    squad_number: int = Path(..., title="The Squad Number of the Player"),
    async_session: AsyncSession = Depends(generate_async_session),
):
    """
    Endpoint to retrieve a Player by its Squad Number.

    Args:
        squad_number (int): The Squad Number of the Player to retrieve.
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Returns:
        PlayerResponseModel: The Pydantic model representing the matching Player.

    Raises:
        HTTPException: HTTP 404 Not Found error if the Player with the specified
        Squad Number does not exist.
    """
    player = await player_service.retrieve_by_squad_number_async(
        async_session, squad_number
    )
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return player


# PUT --------------------------------------------------------------------------


@api_router.put(
    "/players/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Updates an existing Player",
    tags=["Players"],
)
async def put_async(
    player_id: UUID = Path(..., title="The UUID of the Player"),
    player_model: PlayerRequestModel = Body(...),
    async_session: AsyncSession = Depends(generate_async_session),
):
    """
    Endpoint to entirely update an existing Player.

    Args:
        player_id (UUID): The UUID of the Player to update.
        player_model (PlayerRequestModel): The Pydantic model representing the Player
        to update.
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Raises:
        HTTPException: HTTP 404 Not Found error if the Player with the specified UUID
        does not exist.
    """
    player = await player_service.retrieve_by_id_async(async_session, player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    updated = await player_service.update_async(async_session, player_id, player_model)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update the Player due to a database error.",
        )
    await simple_memory_cache.clear(CACHE_KEY)


# DELETE -----------------------------------------------------------------------


@api_router.delete(
    "/players/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes an existing Player",
    tags=["Players"],
)
async def delete_async(
    player_id: UUID = Path(..., title="The UUID of the Player"),
    async_session: AsyncSession = Depends(generate_async_session),
):
    """
    Endpoint to delete an existing Player.

    Args:
        player_id (UUID): The UUID of the Player to delete.
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Raises:
        HTTPException: HTTP 404 Not Found error if the Player with the specified UUID
        does not exist.
    """
    player = await player_service.retrieve_by_id_async(async_session, player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    deleted = await player_service.delete_async(async_session, player_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete the Player due to a database error.",
        )
    await simple_memory_cache.clear(CACHE_KEY)

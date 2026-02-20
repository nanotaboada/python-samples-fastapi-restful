"""
Async CRUD operations for Player entities using SQLAlchemy ORM.

Functions:
- create_async                   : Add a new Player to the database.
- retrieve_all_async             : Fetch all Player records.
- retrieve_by_id_async           : Fetch a Player by its UUID
                                   (surrogate key, internal).
- retrieve_by_squad_number_async : Fetch a Player by its Squad Number
                                   (natural key, domain).
- update_async                   : Fully update an existing Player.
- delete_async                   : Remove a Player from the database.

Handles SQLAlchemy exceptions with transaction rollback and logs errors.
"""

import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from models.player_model import PlayerRequestModel
from schemas.player_schema import Player

# https://github.com/encode/uvicorn/issues/562
logger = logging.getLogger("uvicorn.error")

# Create -----------------------------------------------------------------------


async def create_async(
    async_session: AsyncSession, player_model: PlayerRequestModel
) -> Optional[Player]:
    """
    Creates a new Player in the database.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        player_model (PlayerRequestModel): The Pydantic model representing the Player
        to create.

    Returns:
        The created Player ORM object with its generated UUID, or None on failure.
    """
    # https://docs.pydantic.dev/latest/concepts/serialization/#modelmodel_dump
    player = Player(**player_model.model_dump())
    async_session.add(player)
    try:
        await async_session.commit()
        await async_session.refresh(player)
        return player
    except SQLAlchemyError as error:
        logger.exception("Error trying to create the Player: %s", error)
        await async_session.rollback()
        return None


# Retrieve ---------------------------------------------------------------------


async def retrieve_all_async(async_session: AsyncSession):
    """
    Retrieves all the players from the database.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.

    Returns:
        A collection with all the players.
    """
    # https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-usage
    statement = select(Player)
    result = await async_session.execute(statement)
    players = result.scalars().all()
    return players


async def retrieve_by_id_async(
    async_session: AsyncSession, player_id: UUID
) -> Optional[Player]:
    """
    Retrieves a Player by its UUID from the database.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        player_id (UUID): The UUID of the Player to retrieve.

    Returns:
        The Player matching the provided UUID, or None if not found.
    """
    player = await async_session.get(Player, player_id)
    return player


async def retrieve_by_squad_number_async(
    async_session: AsyncSession, squad_number: int
) -> Optional[Player]:
    """
    Retrieves a Player by its Squad Number from the database.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        squad_number (int): The Squad Number of the Player to retrieve.

    Returns:
        The Player matching the provided Squad Number, or None if not found.
    """
    statement = select(Player).where(Player.squad_number == squad_number)
    result = await async_session.execute(statement)
    player = result.scalars().first()
    return player


# Update -----------------------------------------------------------------------


async def update_async(
    async_session: AsyncSession, player_id: UUID, player_model: PlayerRequestModel
) -> bool:
    """
    Updates (entirely) an existing Player in the database.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        player_id (UUID): The UUID of the Player to update.
        player_model (PlayerRequestModel): The Pydantic model representing the Player
        to update.

    Returns:
        True if the Player was updated successfully, False otherwise.
    """
    player = await async_session.get(Player, player_id)
    player.first_name = player_model.first_name
    player.middle_name = player_model.middle_name
    player.last_name = player_model.last_name
    player.date_of_birth = player_model.date_of_birth
    player.squad_number = player_model.squad_number
    player.position = player_model.position
    player.abbr_position = player_model.abbr_position
    player.team = player_model.team
    player.league = player_model.league
    player.starting11 = player_model.starting11
    try:
        await async_session.commit()
        return True
    except SQLAlchemyError as error:
        logger.exception("Error trying to update the Player: %s", error)
        await async_session.rollback()
        return False


# Delete -----------------------------------------------------------------------


async def delete_async(async_session: AsyncSession, player_id: UUID) -> bool:
    """
    Deletes an existing Player from the database.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        player_id (UUID): The UUID of the Player to delete.

    Returns:
        True if the Player was deleted successfully, False otherwise.
    """
    player = await async_session.get(Player, player_id)
    await async_session.delete(player)
    try:
        await async_session.commit()
        return True
    except SQLAlchemyError as error:
        logger.exception("Error trying to delete the Player: %s", error)
        await async_session.rollback()
        return False

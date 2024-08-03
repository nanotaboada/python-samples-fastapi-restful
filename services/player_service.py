# ------------------------------------------------------------------------------
# Service
# ------------------------------------------------------------------------------

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from models.player_model import PlayerModel
from schemas.player_schema import Player

# Create -----------------------------------------------------------------------


async def create_async(async_session: AsyncSession, player_model: PlayerModel):
    """
    Creates a new Player in the database.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        player_model (PlayerModel): The Pydantic model representing the Player to create.

    Returns:
        True if the Player was created successfully, False otherwise.
    """
    # https://docs.pydantic.dev/latest/concepts/serialization/#modelmodel_dump
    player = Player(**player_model.model_dump())
    async_session.add(player)
    try:
        await async_session.commit()
        return True
    except SQLAlchemyError as error:
        print(f"Error trying to create the Player: {error}")
        await async_session.rollback()
        return False

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


async def retrieve_by_id_async(async_session: AsyncSession, player_id: int):
    """
    Retrieves a Player by its ID from the database.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        player_id (int): The ID of the Player to retrieve.

    Returns:
        The Player matching the provided ID, or None if not found.
    """
    player = await async_session.get(Player, player_id)
    return player


async def retrieve_by_squad_number_async(async_session: AsyncSession, squad_number: int):
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


async def update_async(async_session: AsyncSession, player_model: PlayerModel):
    """
    Updates (entirely) an existing Player in the database.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        player_model (PlayerModel): The Pydantic model representing the Player to update.

    Returns:
        True if the Player was updated successfully, False otherwise.
    """
    player_id = player_model.id  # Extract ID from player_model
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
        print(f"Error trying to update the Player: {error}")
        await async_session.rollback()
        return False

# Delete -----------------------------------------------------------------------


async def delete_async(async_session: AsyncSession, player_id: int):
    """
    Deletes an existing Player from the database.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        player_id (int): The ID of the Player to delete.

    Returns:
        True if the Player was deleted successfully, False otherwise.
    """
    player = await async_session.get(Player, player_id)
    await async_session.delete(player)
    try:
        await async_session.commit()
        return True
    except SQLAlchemyError as error:
        print(f"Error trying to delete the Player: {error}")
        await async_session.rollback()
        return False

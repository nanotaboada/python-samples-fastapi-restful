# ------------------------------------------------------------------------------
# Service
# ------------------------------------------------------------------------------

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.player_model import PlayerModel
from schemas.player_schema import Player

# Create -----------------------------------------------------------------------


def create(orm_session: Session, player_model: PlayerModel):
    """Creates a new Player in the database.

    Args:
        orm_session: The SQLAlchemy ORM session instance.
        player_model: The Pydantic model instance representing a Player.

    Returns:
        True if the Player was created successfully, False otherwise.
    """
    # https://docs.pydantic.dev/latest/concepts/serialization/#modelmodel_dump
    player = Player(**player_model.model_dump())
    orm_session.add(player)
    try:
        orm_session.commit()
        return True
    except SQLAlchemyError as error:
        print(f"Error trying to create the Player: {error}")
        orm_session.rollback()
        return False

# Retrieve ---------------------------------------------------------------------


def retrieve_all(orm_session: Session):
    """Retrieves all the players from the database.

    Args:
        orm_session: The SQLAlchemy ORM session instance.

    Returns:
        A collection with all the players.
    """
    # https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-usage
    statement = select(Player)
    players = orm_session.execute(statement).scalars().all()
    return players


def retrieve_by_id(orm_session: Session, player_id: int):
    """Retrieves a Player by its ID from the database.

    Args:
        orm_session: The SQLAlchemy ORM session instance.
        player_id: The ID of the Player.

    Returns:
        The Player matching the provided ID, or None if not found.
    """
    player = orm_session.get(Player, player_id)
    return player


def retrieve_by_squad_number(orm_session: Session, squad_number: int):
    """Retrieves a Player by its Squad Number from the database.

    Args:
        orm_session: The SQLAlchemy ORM session instance.
        squad_number: The Squad Number of the Player.

    Returns:
        The Player matching the provided Squad Number, or None if not found.
    """
    statement = select(Player).where(Player.squad_number == squad_number)
    player = orm_session.execute(statement).scalars().first()
    return player

# Update -----------------------------------------------------------------------


def update(orm_session: Session, player_model: PlayerModel):
    """Updates an existing Player in the database.

    Args:
        orm_session: The SQLAlchemy ORM session instance.
        player_model: The Pydantic model instance representing a Player.

    Returns:
        True if the Player was updated successfully, False otherwise.
    """
    player_id = player_model.id  # Extract ID from player_model
    player = orm_session.get(Player, player_id)
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
        orm_session.commit()
        return True
    except SQLAlchemyError as error:
        print(f"Error trying to update the Player: {error}")
        orm_session.rollback()
        return False

# Delete -----------------------------------------------------------------------


def delete(orm_session: Session, player_id: int):
    """Deletes a Player from the database.

    Args:
        orm_session: The SQLAlchemy ORM session instance.
        player_id: The ID of the Player.

    Returns:
        True if the Player was deleted successfully, False otherwise.
    """
    player = orm_session.get(Player, player_id)
    orm_session.delete(player)
    try:
        orm_session.commit()
        return True
    except SQLAlchemyError as error:
        print(f"Error trying to delete the Player: {error}")
        orm_session.rollback()
        return False

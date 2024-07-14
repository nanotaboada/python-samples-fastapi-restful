# ------------------------------------------------------------------------------
# Schema
# ------------------------------------------------------------------------------

from sqlalchemy import Column, String, Integer, Boolean
from data.player_database import Base


class Player(Base):
    """
    SQLAlchemy schema describing a database table of football players.

    Attributes:
        id (Integer): The primary key for the player record.
        first_name (String): The first name of the player (not nullable).
        middle_name (String): The middle name of the player.
        last_name (String): The last name of the player (not nullable).
        date_of_birth (String): The date of birth of the player.
        squad_number (Integer): The squad number of the player (not nullable, unique).
        position (String): The playing position of the player (not nullable).
        abbr_position (String): The abbreviated form of the player's position.
        team (String): The team to which the player belongs.
        league (String): The league where the team plays.
        starting11 (Boolean): Indicates if the player is in the starting 11.
    """

    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, name='firstName', nullable=False)
    middle_name = Column(String, name='middleName')
    last_name = Column(String, name='lastName', nullable=False)
    date_of_birth = Column(String, name="dateOfBirth")
    squad_number = Column(Integer, name='squadNumber', unique=True, nullable=False)
    position = Column(String, nullable=False)
    abbr_position = Column(String, name='abbrPosition')
    team = Column(String)
    league = Column(String)
    starting11 = Column(Boolean)

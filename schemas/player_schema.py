# -------------------------------------------------------------------------------------------------
# Schema
# -------------------------------------------------------------------------------------------------

from sqlalchemy import Column, String, Integer, Boolean
from data.player_database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column('firstName', String, nullable=False)
    middle_name = Column('middleName', String)
    last_name = Column('lastName', String, nullable=False)
    date_of_birth = Column('dateOfBirth')
    squad_number = Column('squadNumber', Integer, index=True, nullable=False)
    position = Column('position', String, nullable=False)
    abbr_position = Column('abbrPosition', String)
    team = Column('team', String)
    league = Column('league', String)
    starting11 = Column('starting11', Boolean)

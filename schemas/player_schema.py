# -------------------------------------------------------------------------------------------------
# Schema
# -------------------------------------------------------------------------------------------------

from sqlalchemy import Column, String, Integer, Boolean
from data.player_database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, name='firstName', nullable=False)
    middle_name = Column(String, name='middleName')
    last_name = Column(String, name='lastName', nullable=False)
    date_of_birth = Column(String, name="dateOfBirth")
    squad_number = Column(Integer, name='squadNumber', index=True, nullable=False)
    position = Column(String, nullable=False)
    abbr_position = Column(String, name='abbrPosition')
    team = Column(String)
    league = Column(String)
    starting11 = Column(Boolean)

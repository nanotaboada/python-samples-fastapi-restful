# -------------------------------------------------------------------------------------------------
# Models
# -------------------------------------------------------------------------------------------------


from sqlalchemy import Column, String, Integer, Boolean
from data.player_database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)
    middleName = Column(String, index=True)
    lastName = Column(String, index=True)
    dateOfBirth = Column(String, index=True)
    squadNumber = Column(Integer, index=True)
    position = Column(String, index=True)
    abbrPosition = Column(String, index=True)
    team = Column(String, index=True)
    league = Column(String, index=True)
    starting11 = Column(Boolean, index=True)

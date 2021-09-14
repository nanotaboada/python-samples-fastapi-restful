# models.py

from sqlalchemy import Column, String, Integer
from data.database import Base


class Song(Base):
    __tablename__ = "songs"

    rank = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String, index=True)
    album = Column(String, index=True)
    year = Column(Integer, index=True)

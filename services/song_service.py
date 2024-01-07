# -------------------------------------------------------------------------------------------------
# Services
# -------------------------------------------------------------------------------------------------

from sqlalchemy.orm import Session
from models.song_model import Song


# Retrieve


def retrieve_all_songs(db: Session):
    return db.query(Song).all()


def retrieve_songs_by_year(db: Session, year: int):
    return db.query(Song).filter(Song.year == year).all()


def retrieve_song_by_rank(db: Session, rank: int):
    return db.query(Song).filter(Song.rank == rank).first()

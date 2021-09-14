# services.py

from sqlalchemy.orm import Session
from models import models

# TODO: Create, Update, Delete


# Retrieve
def retrieve_all_songs(db: Session):
    return db.query(models.Song).all()


def retrieve_songs_by_year(db: Session, year: int):
    return db.query(models.Song).filter(models.Song.year == year).all()


def retrieve_song_by_rank(db: Session, rank: int):
    return db.query(models.Song).filter(models.Song.rank == rank).first()

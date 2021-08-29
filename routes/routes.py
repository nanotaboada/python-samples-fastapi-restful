# routes.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from data.database import OrmSession
from sqlalchemy.orm import Session
from schemas import schemas
from services import services

api_router = APIRouter()


# We need to have an independent database session/connection per request, use
# the same session through all the request and then close it after the request
# is finished.
# And then a new session will be created for the next request.
# Our dependency will create a new SQLAlchemy Session that will be used in a
# single request, and then close it once the request is finished.
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
def get_db_session():
    db_session = OrmSession()
    try:
        yield db_session
    finally:
        db_session.close()

# TODO: HTTP POST, HTTP PUT and HTTP DELETE


# HTTP GET
@api_router.get("/songs/", response_model=List[schemas.Song])
def get_songs(db_session: Session = Depends(get_db_session)):
    songs = services.retrieve_all_songs(db_session)
    if songs is None:
        raise HTTPException(status_code=404)
    return songs


@api_router.get("/songs/year/{year}", response_model=List[schemas.Song])
def get_songs_by_year(year: str, db_session: Session = Depends(get_db_session)):
    songs = services.retrieve_songs_by_year(db_session, year=year)
    if songs is None:
        raise HTTPException(status_code=404)
    return songs


@api_router.get("/songs/rank/{rank}", response_model=schemas.Song)
def get_song_by_rank(rank: int, db_session: Session = Depends(get_db_session)):
    song = services.retrieve_song_by_rank(db_session, rank=rank)
    if song is None:
        raise HTTPException(status_code=404)
    return song

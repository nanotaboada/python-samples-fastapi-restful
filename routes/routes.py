# routes.py

from fastapi import APIRouter, Depends, HTTPException, status, Path
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
@api_router.get(
    "/songs/",
    response_model=List[schemas.Song],
    summary="Gets all songs in the collection"
)
def get_songs(
    db_session: Session = Depends(get_db_session)
):
    songs = services.retrieve_all_songs(db_session)
    return songs


@api_router.get(
    "/songs/year/{year}",
    response_model=List[schemas.Song],
    summary="Gets all songs from the specified year"
)
def get_songs_by_year(
    year: int = Path(..., title="The year of the songs to get", ge=1948, le=2009),
    db_session: Session = Depends(get_db_session)
):
    songs = services.retrieve_songs_by_year(db_session, year=year)
    if not songs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return songs


@api_router.get(
    "/songs/rank/{rank}",
    response_model=schemas.Song,
    summary="Get the song with the specified rank"
)
def get_song_by_rank(
    rank: int = Path(..., title="The rank of the song to get", ge=1, le=500),
    db_session: Session = Depends(get_db_session)
):
    song = services.retrieve_song_by_rank(db_session, rank=rank)
    return song

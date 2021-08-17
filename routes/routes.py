# routes.py

from fastapi import APIRouter, Depends, HTTPException
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
@api_router.get("/books/{isbn}", response_model=schemas.Book)
def get_book(isbn: str, db_session: Session = Depends(get_db_session)):
    book = services.retrieve_book_by_isbn(db_session, isbn=isbn)
    if book is None:
        raise HTTPException(status_code=404)
    return book


@api_router.get("/catalog/init", status_code=200)
def init(db_session: Session = Depends(get_db_session)):
    services.reset_catalog(db_session)
    return {"detail": "Catalog initialized."}


@api_router.get("/catalog/reset", status_code=200)
def reset(db_session: Session = Depends(get_db_session)):
    services.init_catalog(db_session)
    return {"detail": "Catalog reset."}

# routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from data.database import SessionLocal, engine
from schemas import schemas
from models import models
from services import crud

api_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api_router.get("/books/{isbn}", response_model=schemas.Book)
def get_book(isbn: str, db: Session = Depends(get_db)):
    book = crud.retrieve_book_by_isbn(db, isbn=isbn)
    if book is None:
        raise HTTPException(status_code=404)
    return book


# TODO: Implement migrations with Alembic
# https://github.com/nanotaboada/python-samples-fastapi-restful/issues/2
models.Base.metadata.create_all(bind=engine)


@api_router.get("/catalog/init", status_code=200)
def init(db: Session = Depends(get_db)):
    crud.reset_catalog(db)
    return {"detail": "Catalog initialized."}


@api_router.get("/catalog/reset", status_code=200)
def reset(db: Session = Depends(get_db)):
    crud.init_catalog(db)
    return {"detail": "Catalog reset."}

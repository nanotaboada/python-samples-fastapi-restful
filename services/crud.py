# crud.py

from sqlalchemy.orm import Session
from models import models
from datetime import datetime

# TODO: Implement migrations with Alembic
# https://github.com/nanotaboada/python-samples-fastapi-restful/issues/2
book_to_create = models.Book(
    isbn="9781430224150",
    title="Dive into Python 3",
    subtitle="All you need to know to get off the ground with Python 3",
    author="Mark Pilgrim",
    published=datetime(2009, 1, 1),
    publisher="Apress",
    pages=360,
    description="Mark Pilgrim's Dive Into Python 3 is a hands-on guide to Python 3 and its differences from Python 2. As in the original book, Dive Into Python, each chapter starts with a real, complete code sample, proceeds to pick it apart and explain the pieces, and then puts it all back together in a summary at the end.",
    website="https://diveintopython3.net"
)


def init_catalog(db: Session):
    db.add(book_to_create)
    db.commit()


def reset_catalog(db: Session):
    book_to_delete = db.query(models.Book).filter(models.Book.isbn == "9781430224150").first()
    db.delete(book_to_delete)
    db.commit()


def retrieve_book_by_isbn(db: Session, isbn: str):
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()

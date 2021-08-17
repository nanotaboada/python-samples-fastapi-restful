# models.py

from sqlalchemy import Column, String, Integer, DateTime
from data.database import Base


class Book(Base):
    __tablename__ = "books"

    isbn = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    subtitle = Column(String, index=True)
    author = Column(String, index=True)
    published = Column(DateTime, index=True)
    publisher = Column(String, index=True)
    pages = Column(Integer, index=True)
    description = Column(String, index=True)
    website = Column(String, index=True)

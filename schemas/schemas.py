# schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Book(BaseModel):
    isbn: str
    title: str
    subtitle: Optional[str] = None
    author: str
    published: datetime
    publisher: str
    pages: int
    description: str
    website: str

    class Config:
        orm_mode = True

from fastapi import APIRouter
from data.catalog import books

router = APIRouter()

@router.get("/books")
def read_books():
    return books
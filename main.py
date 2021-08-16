from fastapi import FastAPI
from routes import books

fast_api = FastAPI()
fast_api.include_router(books.router)
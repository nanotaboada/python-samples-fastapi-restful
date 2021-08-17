# main.py

from fastapi import FastAPI
from routes import routes

app = FastAPI()

fast_api = FastAPI()
fast_api.include_router(routes.api_router)

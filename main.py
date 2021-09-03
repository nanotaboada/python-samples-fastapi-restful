# main.py

from fastapi import FastAPI
from routes import routes

fast_api = FastAPI()
fast_api.include_router(routes.api_router)

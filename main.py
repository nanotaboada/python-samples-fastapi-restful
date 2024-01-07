# -------------------------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------------------------

from fastapi import FastAPI
from routes import song_route

fast_api = FastAPI()
fast_api.include_router(song_route.api_router)

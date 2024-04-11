# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------

from fastapi import FastAPI
from routes import player_route

app = FastAPI()
app.include_router(player_route.api_router)

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------

from contextlib import asynccontextmanager
import logging
from typing import AsyncIterator
from fastapi import FastAPI
from routes import player_route, health_route

# https://github.com/encode/uvicorn/issues/562
UVICORN_LOGGER = "uvicorn.error"
logger = logging.getLogger(UVICORN_LOGGER)

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """"
    Lifespan event handler for FastAPI.
    """
    logger.info("Lifespan event handler execution complete.")
    yield

app = FastAPI(lifespan=lifespan,
              title="python-samples-fastapi-restful",
              description="🧪 Proof of Concept for a RESTful API made with Python 3 and FastAPI",
              version="1.0.0",)

app.include_router(player_route.api_router)
app.include_router(health_route.api_router)

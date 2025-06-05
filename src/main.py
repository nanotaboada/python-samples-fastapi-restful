"""
Main application module for the FastAPI RESTful API.

- Sets up the FastAPI app with metadata (title, description, version).
- Defines the lifespan event handler for app startup/shutdown logging.
- Includes API routers for player and health endpoints.

This serves as the entry point for running the API server.
"""

from contextlib import asynccontextmanager
import logging
from typing import AsyncIterator
from fastapi import FastAPI
from src.routes import player, health

# https://github.com/encode/uvicorn/issues/562
UVICORN_LOGGER = "uvicorn.error"
logger = logging.getLogger(UVICORN_LOGGER)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """
    Lifespan event handler for FastAPI.
    """
    logger.info("Lifespan event handler execution complete.")
    yield


app = FastAPI(
    lifespan=lifespan,
    title="python-samples-fastapi-restful",
    description="🧪 Proof of Concept for a RESTful API made with Python 3 and FastAPI",
    version="1.0.0",
)

app.include_router(player.router)
app.include_router(health.router)

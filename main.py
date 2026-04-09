"""
Main application module for the FastAPI RESTful API.

- Sets up the FastAPI app with metadata (title, description, version).
- Defines the lifespan event handler for app startup/shutdown logging.
- Includes API routers for player and health endpoints.

This serves as the entry point for running the API server.
"""

import asyncio
from contextlib import asynccontextmanager
import logging
from typing import AsyncIterator
from alembic.config import Config
from alembic import command
from fastapi import FastAPI
from routes import player_route, health_route

# https://github.com/encode/uvicorn/issues/562
UVICORN_LOGGER = "uvicorn.error"
logger = logging.getLogger(UVICORN_LOGGER)


def _apply_migrations() -> None:
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """
    Lifespan event handler for FastAPI.

    Runs database migrations before the application starts accepting requests.
    Alembic is invoked in a thread executor to avoid conflicts with the running
    event loop (alembic's async env.py calls asyncio.run() internally).
    """
    logger.info("Applying database migrations...")
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _apply_migrations)
    logger.info("Database migrations applied successfully.")
    yield


app = FastAPI(
    lifespan=lifespan,
    title="python-samples-fastapi-restful",
    description="🧪 Proof of Concept for a RESTful API made with Python 3 and FastAPI",
    version="1.0.0",
)

app.include_router(player_route.api_router)
app.include_router(health_route.api_router)

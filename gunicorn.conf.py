"""
Gunicorn configuration for production deployment.

Uses UvicornWorker to run the FastAPI ASGI app. The on_starting hook runs
Alembic migrations once in the master process before any workers are forked,
ensuring a single, race-free initialization step.
"""

import multiprocessing
import os
from pathlib import Path

from alembic import command
from alembic.config import Config

bind: str = "0.0.0.0:9000"
workers: int = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))
worker_class: str = "uvicorn.workers.UvicornWorker"


def on_starting(server) -> None:
    """Apply Alembic migrations once before workers are spawned."""
    alembic_cfg = Config(str(Path(__file__).resolve().parent / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

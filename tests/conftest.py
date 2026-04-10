import warnings
from pathlib import Path
from typing import Any, Generator

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from main import app
from tests.player_fake import Player, nonexistent_player

# Suppress the DeprecationWarning from httpx
warnings.filterwarnings("ignore", category=DeprecationWarning)

ALEMBIC_CONFIG = Config(str(Path(__file__).resolve().parent.parent / "alembic.ini"))


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """Apply Alembic migrations once before the test session starts."""
    command.upgrade(ALEMBIC_CONFIG, "head")


@pytest.fixture(scope="function")
def client():
    """
    Creates a test client for the FastAPI app.

    This fixture provides a fresh instance of TestClient for each test function,
    ensuring test isolation and a clean request context.

    Yields:
        TestClient: A client instance for sending HTTP requests to the FastAPI app.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def nonexistent_player_in_db(client: Any) -> Generator[Player, None, None]:
    """
    Creates the nonexistent player in the database and removes it on teardown.

    Yields:
        Player: The fake player created in the database.
    """
    player: Player = nonexistent_player()
    client.post("/players/", json=player.__dict__)
    yield player
    client.delete(f"/players/squadnumber/{player.squad_number}")

import warnings
from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from main import app
from tests.player_fake import Player, nonexistent_player

# Suppress the DeprecationWarning from httpx
warnings.filterwarnings("ignore", category=DeprecationWarning)


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
        Player: The player stub created in the database.
    """
    player: Player = nonexistent_player()
    client.post("/players/", json=player.__dict__)
    yield player
    client.delete(f"/players/squadnumber/{player.squad_number}")

import warnings
import pytest
from fastapi.testclient import TestClient
from src.main import app

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

import pytest
import warnings
from fastapi.testclient import TestClient
from main import app

# Suppress the DeprecationWarning from httpx
warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

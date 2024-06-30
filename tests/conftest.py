import warnings
import pytest
from fastapi.testclient import TestClient
from main import app

# Suppress the DeprecationWarning from httpx
warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

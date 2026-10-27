"""
Fixtures for the unit tests.
"""

import pytest


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """Disable database migrations for unit tests."""
    pass

"""Base classes for pytest."""
import pytest
import app

@pytest.fixture
def testapp():
    """Provide the rover service."""
    return app

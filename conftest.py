"""Base classes for pytest."""
import pytest
import rovercode.app as app

@pytest.fixture
def testapp():
    """Provide the rover service."""
    return app

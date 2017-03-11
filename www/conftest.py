"""Base classes for pytest."""
import pytest
from app import create_app

@pytest.fixture
def app():
    """Create the rovercode Flask app."""
    app = create_app()
    return app

"""A dummy binary sensor that returns random values."""

import random
import logging

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))


class DummyBinarySensor:
    """A sensor that returns random values."""

    def __init__(self):
        """Create the dummy sensor."""
        LOGGER.info("Created dummy binary sensor")

    def is_high(self):
        """Return true or false randomly."""
        return random.choice([True, False])

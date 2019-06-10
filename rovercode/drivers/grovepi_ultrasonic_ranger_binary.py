"""
Class for communicating with the GrovePi ultrasonic ranger.

Here we treat it as a binary sensor.
"""

import os
import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))
if os.getenv('DEVELOPMENT', 'false').lower() == 'true':
    LOGGER.warning("Running in DEVELOPMENT mode. Using dummy.")
    from drivers.dummy_grovepi_interface import ultrasonicRead
else:
    from grovepi import ultrasonicRead  # noqa


class GrovePiUltrasonicRangerBinary:
    """A module to read from the GrovePi Ultrasonic as a binary sensor."""

    def __init__(self, port, binary_threshold):
        """Create a GrovePi Ultrasonic Ranger (Binary) driver module."""
        self.port = int(port)
        self.binary_threshold = binary_threshold
        LOGGER.info("Setting up GrovePi Ultrasonic Binary Ranger on port %s",
                    port)

    def is_high(self):
        """HIGH, meaning "seeing something"."""
        # False output means no object detected
        # True output means object detected
        return ultrasonicRead(self.port) < self.binary_threshold

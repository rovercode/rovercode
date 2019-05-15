"""
Class for communicating with the GrovePi ultrasonic ranger.

Here we treat it as a binary sensor.
"""

import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))
try:
    from grovepi import ultrasonicRead
except ImportError:
    LOGGER.warning("GrovePi lib unavailable. Using dummy.")
    from drivers.dummy_grovepi_interface import ultrasonicRead


class GrovePiUltrasonicRangerBinary:
    """A module to read from the GrovePi Ultrasonic as a binary sensor."""

    def __init__(self, port, binary_threshold):
        """Create a GrovePi Ultrasonic Ranger (Binary) driver module."""
        self.port = int(port)
        self.binary_threshold = binary_threshold
        print(f"Setting up GrovePi Ultrasonic Ranger (Binary) on port {port}")

    def is_high(self):
        """HIGH, meaning "seeing something"."""
        # False output means no object detected
        # True output means object detected
        return ultrasonicRead(self.port) < self.binary_threshold

"""
Class for communicating with the GrovePi ultrasonic ranger.

Here we treat it as a binary sensor.
"""

import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))
try:
    from GrovePi.Software.Python.grovepi import ultrasonicRead
except ImportError:
    LOGGER.warn("GrovePi lib unavailable. Using dummy.")
    from drivers.dummy_grovepi_interface import ultrasonicRead


class GrovePiUltrasonicRangerBinary:
    """A module to read from the GrovePi Ultrasonic as a binary sensor."""

    def __init__(self, port, binary_threshold):
        """Create a GrovePi Ultrasonic Ranger (Binary) driver module."""
        self.port = int(port)
        self.binary_threshold = binary_threshold
        print("Setting up GrovePi Ultrasonic Ranger (Binary) on port"
              .format(port))

    def is_high(self):
        """HIGH, meaning "not seeing something"."""
        # to match the old GPIO sensors, we'll make this sensor active low
        # False output means object detected
        # True output means no object detected
        return ultrasonicRead(self.port) > self.binary_threshold

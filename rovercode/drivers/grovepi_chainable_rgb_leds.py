"""
Class for communicating with the GrovePi ultrasonic ranger.

Here we treat it as a binary sensor.
"""

import logging
import time

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))
try:
    from GrovePi.Software.Python.grovepi import chainableRgbLed_pattern,\
        storeColor, chainableRgbLed_init, pinMode
except ImportError:
    LOGGER.warning("GrovePi lib unavailable. Using dummy.")
    from drivers.dummy_grovepi_interface import chainableRgbLed_pattern,\
        storeColor, chainableRgbLed_init, pinMode


class GrovePiChainableRgbLeds:
    """A module to set the GrovePi Chainable RGB LEDs."""

    MODE_THIS_LED_ONLY = 0
    port = None

    def setup(self, port, count):
        """Create a GrovePi Chainable RGB LEDs module."""
        self.port = int(port)
        pinMode(port, "OUTPUT")
        time.sleep(1)
        chainableRgbLed_init(self.port, count)
        LOGGER.info("Setting up %s GrovePi Chainable RGB LEDs on port %s",
                    count, port)

    def set_color(self, led, red, green, blue):
        """Set color in RGB, each ranged 0-255."""
        if self.port is None:
            raise RuntimeError("Must call setup before setting color.")

        for component in (red, green, blue):
            if not 0 <= component <= 255:
                LOGGER.error("RGB color value %s not in range 0-255.")
                return
        storeColor(red, green, blue)
        time.sleep(.1)
        chainableRgbLed_pattern(self.port, self.MODE_THIS_LED_ONLY, led)
        time.sleep(.1)

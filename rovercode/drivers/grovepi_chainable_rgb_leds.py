"""Class for communicating with a GrovePi chainable RGB LED."""

import os
import logging
import time

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))
if os.getenv('DEVELOPMENT', 'false').lower() == 'true':
    LOGGER.warning("In DEVELOPMENT mode. Using dummy.")
    from drivers.dummy_grovepi_interface import chainableRgbLed_pattern, \
        storeColor, chainableRgbLed_init, pinMode
else:
    from grovepi import chainableRgbLed_pattern, \
        storeColor, chainableRgbLed_init, pinMode


class GrovePiChainableRgbLeds:
    """A module to set the GrovePi Chainable RGB LEDs."""

    MODE_THIS_LED_ONLY = 0
    COMPONENT_RANGE = 0, 256

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
        """Set color in RGB."""
        if self.port is None:
            raise RuntimeError("Must call setup before setting color.")

        for component in (red, green, blue):
            if component not in self.COMPONENT_RANGE:
                LOGGER.error(f'RGB color value %s not in range '
                             f'{self.COMPONENT_RANGE[0]}-'
                             f'{self.COMPONENT_RANGE[1]-1}.')
                return
        storeColor(red, green, blue)
        time.sleep(.1)
        chainableRgbLed_pattern(self.port, self.MODE_THIS_LED_ONLY, led)
        time.sleep(.1)

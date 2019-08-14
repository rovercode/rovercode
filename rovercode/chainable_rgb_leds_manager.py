"""Class for managing the motor state."""

import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))


class ChainableRgbLedsManager:
    """Object to manage RGB LEDs."""

    def __init__(self, port, count, driver):
        """Construct a RgbLedManager."""
        self.port = port
        self.count = count
        self.driver = driver
        self.driver.setup(port, self.count)
        LOGGER.info("RGB LED manager initialized")

    def set_led_color(self, led, red, green, blue):
        """Set LED color."""
        if led > self.count - 1:
            LOGGER.error("Unknown led %s", led)
            return

        for component in (red, green, blue):
            if not 0 <= component <= 255:
                LOGGER.error("RGB color value %s not in range 0-255.")
                return

        LOGGER.info("Setting LED %s to %s, %s, %s.",
                    led, red, green, blue)
        self.driver.set_rgb(led, red, green, blue)

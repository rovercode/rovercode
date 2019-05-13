"""Class for managing the motor state."""

import logging
from constants import \
    LEFT_MOTOR, RIGHT_MOTOR,\
    MOTOR_DIRECTION_FORWARD, MOTOR_DIRECTION_BACKWARD
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))


class ChainableRgbLedsManager:
    """Object to manage RGB LEDs."""

    def __init__(self, port, user_led_count, driver):
        """Construct a RgbLedManager.

        Keeps track of one status LED and a configurable number of
        user-settable LEDs.
        """
        self.port = port
        self.count = 1 + user_led_count
        self.driver = driver
        self.driver.setup(port, self.count)
        LOGGER.info("RGB LED manager initialized")

    def set_status_led_color(self, r, g, b):
        self.set_led_color(0, r, g, b)

    def set_user_led_color(self, user_led, r, g, b):
        self.set_led_color(user_led + 1, r, g, b)

    def set_led_color(self, led, r, g, b):
        """Set the speed of a motor pin."""
        if led > self.count - 1:
            LOGGER.error("Unknown led %s", led)
            return

        for component in (r, g, b):
            if not 0 <= component <= 255:
                LOGGER.error("RGB color value %s not in range 0-255.")
                return

        LOGGER.info("Setting LED %s to %s, %s, %s.",
                    led, r, g, b)
        self.driver.set_rgb(led, r, g, b)

"""Class for managing the chainable RGB LEDs."""

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

    def set_all_led_colors(self, red, green, blue):
        """Set all LEDs to the same color."""
        for led in range(self.count):
            self.set_led_color(led, red, green, blue)

    def set_led_color(self, led, red, green, blue):
        """Set LED color."""
        if led not in range(self.count):
            raise ValueError(f'Unknown led {led}')

        component_range = self.driver.COMPONENT_RANGE
        for component in (red, green, blue):
            if component not in component_range:
                raise ValueError(f'RGB value {component} not in range '
                                 f'{component_range[0]}-{component_range[-1]}')

        LOGGER.info("Setting LED %s to %s, %s, %s.",
                    led, red, green, blue)
        self.driver.set_color(led, red, green, blue)

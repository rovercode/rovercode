"""Test the chainable RGB LED manager."""

import pytest
from mock import MagicMock, call

from chainable_rgb_leds_manager import ChainableRgbLedsManager


@pytest.fixture
def driver_mock():
    """Set up mock of the LED driver."""
    driver = MagicMock()
    driver.COMPONENT_RANGE = range(0, 256)
    return driver


def test_chainable_rgb_set_color(driver_mock):
    """Test setting a color."""
    motor_controller = ChainableRgbLedsManager(3, 1, driver_mock)
    motor_controller.set_led_color(0, 1, 2, 3)
    driver_mock.set_color.assert_called_with(0, 1, 2, 3)


def test_chainable_rgb_set_color_bad_led(driver_mock):
    """Test setting a color with an invalid LED id."""
    num_leds = 1
    motor_controller = ChainableRgbLedsManager(3, num_leds, driver_mock)
    with pytest.raises(ValueError):
        motor_controller.set_led_color(num_leds, 1, 2, 3)


def test_chainable_rgb_set_color_bad_color(driver_mock):
    """Test setting a color with an invalid color value."""
    motor_controller = ChainableRgbLedsManager(3, 1, driver_mock)
    with pytest.raises(ValueError):
        motor_controller.set_led_color(0, 256, 2, 3)


def test_chainable_rgb_set_color_all_leds(driver_mock):
    """Test setting the same color to all LEDs."""
    motor_controller = ChainableRgbLedsManager(3, 2, driver_mock)
    motor_controller.set_all_led_colors(1, 2, 3)
    driver_mock.set_color.assert_has_calls([
        call(0, 1, 2, 3), call(1, 1, 2, 3)])

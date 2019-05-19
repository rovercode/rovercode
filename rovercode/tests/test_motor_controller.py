"""Test the motor controller abstraction."""

import pytest
from mock import MagicMock

from constants import LEFT_MOTOR, RIGHT_MOTOR,\
    MOTOR_DIRECTION_FORWARD, MOTOR_DIRECTION_BACKWARD
from motor_controller import MotorController


@pytest.fixture
def driver_mock():
    """Set up mock of the motor driver."""
    motor_driver = MagicMock()
    motor_driver.DIRECTION_FORWARD = 'driver_forward'
    motor_driver.DIRECTION_BACKWARD = 'driver_backward'
    return motor_driver


def test_motor_controller(driver_mock):
    """Test starting the motors."""
    motor_controller = MotorController(driver_mock)
    motor_controller.set_speed(LEFT_MOTOR, 80, MOTOR_DIRECTION_FORWARD)
    driver_mock.set_left_speed.assert_called_with(80, 'driver_forward')
    motor_controller.set_speed(LEFT_MOTOR, 81, MOTOR_DIRECTION_BACKWARD)
    driver_mock.set_left_speed.assert_called_with(81, 'driver_backward')
    motor_controller.set_speed(RIGHT_MOTOR, 82, MOTOR_DIRECTION_FORWARD)
    driver_mock.set_right_speed.assert_called_with(82, 'driver_forward')
    motor_controller.set_speed(RIGHT_MOTOR, 83, MOTOR_DIRECTION_BACKWARD)
    driver_mock.set_right_speed.assert_called_with(83, 'driver_backward')


def test_motor_controller_negative_value(driver_mock):
    """Test inverting negative speed value."""
    motor_controller = MotorController(driver_mock)
    motor_controller.set_speed(LEFT_MOTOR, -50, MOTOR_DIRECTION_FORWARD)
    driver_mock.set_left_speed.assert_called_with(50, 'driver_backward')
    motor_controller.set_speed(RIGHT_MOTOR, -40, MOTOR_DIRECTION_BACKWARD)
    driver_mock.set_right_speed.assert_called_with(40, 'driver_forward')


def test_motor_controller_bad_motor_name(driver_mock):
    """Test bad motor name."""
    motor_controller = MotorController(driver_mock)
    motor_controller.set_speed('not a real motor', 50, MOTOR_DIRECTION_FORWARD)
    driver_mock.set_speed.assert_not_called()


def test_motor_controller_bad_direction(driver_mock):
    """Test bad direction value."""
    motor_controller = MotorController(driver_mock)
    motor_controller.set_speed(LEFT_MOTOR, 50, 'not a good direction')
    driver_mock.set_speed.assert_not_called()

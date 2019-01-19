"""Test the motor controller abstraction."""

import pytest
from mock import MagicMock, call

from constants import LEFT_MOTOR, RIGHT_MOTOR
from motor_controller import MotorController


def test_motor_controller():
    motor_driver = MagicMock()
    motor_controller = MotorController('1', '2', '3', '4', motor_driver)
    motor_controller.set_speed(LEFT_MOTOR, 80)
    motor_driver.set_speed.assert_called_with('1', 80)
    motor_controller.set_speed(LEFT_MOTOR, -81)
    motor_driver.set_speed.assert_called_with('2', 81)
    motor_controller.set_speed(RIGHT_MOTOR, 82)
    motor_driver.set_speed.assert_called_with('3', 82)
    motor_controller.set_speed(RIGHT_MOTOR, -83)
    motor_driver.set_speed.assert_called_with('4', 83)

def test_motor_controller_left_stop():
    motor_driver = MagicMock()
    motor_controller = MotorController('1', '2', '3', '4', motor_driver)
    motor_controller.set_speed(LEFT_MOTOR, 0)
    motor_driver.set_speed.assert_has_calls([call('1', 0), call('2', 0)])


def test_motor_controller_right_stop():
    motor_driver = MagicMock()
    motor_controller = MotorController('1', '2', '3', '4', motor_driver)
    motor_controller.set_speed(RIGHT_MOTOR, 0)
    motor_driver.set_speed.assert_has_calls([call('3', 0), call('4', 0)])



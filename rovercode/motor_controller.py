"""Class for managing the motor state."""

import logging
from constants import \
    LEFT_MOTOR, RIGHT_MOTOR,\
    MOTOR_DIRECTION_FORWARD, MOTOR_DIRECTION_BACKWARD
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))


class MotorController:
    """Object to manage the motors."""

    def __init__(self, driver, reverse_left=False, reverse_right=False):
        """Construct a MotorManager."""
        self.driver = driver
        self.reverse_left = reverse_left
        self.reverse_right = reverse_right
        LOGGER.info("Motor manager initialized")

    def set_speed(self, motor, speed, direction):
        """Set the speed of a motor pin."""
        if motor not in (LEFT_MOTOR, RIGHT_MOTOR):
            LOGGER.error("Unknown motor %s", motor)
            return

        def reverse_direction(direction):
            return MOTOR_DIRECTION_BACKWARD \
                if direction == MOTOR_DIRECTION_FORWARD \
                else MOTOR_DIRECTION_FORWARD

        try:
            speed = int(speed)
        except ValueError:
            LOGGER.error('Speed %s cannot be parsed as an integer', speed)
            return
        if speed < 0:
            LOGGER.warning("Inverting direction %s because "
                           "of negative motor speed %s",
                           direction, speed)
            speed = abs(speed)
            direction = reverse_direction(direction)
        if (self.reverse_left and motor == LEFT_MOTOR) or \
                (self.reverse_right and motor == RIGHT_MOTOR):
            LOGGER.info("Inverting direction %s of %s per config",
                        direction, motor)
            direction = reverse_direction(direction)

        if direction == MOTOR_DIRECTION_FORWARD:
            driver_direction = self.driver.DIRECTION_FORWARD
        elif direction == MOTOR_DIRECTION_BACKWARD:
            driver_direction = self.driver.DIRECTION_BACKWARD
        else:
            LOGGER.error("Invalid direction %s", direction)
            return

        LOGGER.info("Setting %s to %s with direction %s",
                    motor, speed, direction)
        if motor == LEFT_MOTOR:
            self.driver.set_left_speed(speed, driver_direction)
        else:
            self.driver.set_right_speed(speed, driver_direction)

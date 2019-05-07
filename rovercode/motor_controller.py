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

    def __init__(self, left_port, right_port, driver):
        """Construct a MotorManager."""
        self.ports = {LEFT_MOTOR: left_port, RIGHT_MOTOR: right_port}
        self.driver = driver
        LOGGER.info("Motor manager initialized")

    def set_speed(self, motor, speed, direction):
        """Set the speed of a motor pin."""
        if motor not in self.ports:
            LOGGER.error("Unknown motor %s", motor)
            return

        if speed < 0:
            LOGGER.warning("Inverting direction %s because "
                           "of negative motor speed %s",
                           direction, speed)
            speed = abs(speed)
            direction = MOTOR_DIRECTION_BACKWARD \
                if direction == MOTOR_DIRECTION_FORWARD \
                else MOTOR_DIRECTION_FORWARD

        if direction == MOTOR_DIRECTION_FORWARD:
            driver_direction = self.driver.DIRECTION_FORWARD
        elif direction == MOTOR_DIRECTION_BACKWARD:
            driver_direction = self.driver.DIRECTION_BACKWARD
        else:
            LOGGER.error("Invalid direction %s", direction)
            return

        LOGGER.info("Setting %s to %s with direction %s",
                    motor, speed, direction)
        self.driver.set_speed(self.ports[motor], speed, driver_direction)

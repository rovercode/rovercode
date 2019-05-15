"""Class for communicating with the GrovePi motor controller."""

import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))
try:
    import sys
    sys.path.append('../GrovePi/Software/Python')
    from grove_mini_motor_driver.grove_mini_motor_driver import MiniMotorDriver
    from grove_mini_motor_driver.grove_mini_motor_driver import left_channel, right_channel
except ImportError:
    LOGGER.warning("Grove I2C mini motor driver lib unavailable. Using dummy.")
    from drivers.dummy_grovepi_interface import MiniMotorDriver, left_channel, right_channel


class GroveMotors:
    """Helper functions for setting the GrovePi motor controllers."""

    DIRECTION_FORWARD = 'FORWARD'
    DIRECTION_BACKWARD = 'REVERSE'
    DIRECTIONS = (DIRECTION_FORWARD, DIRECTION_BACKWARD)

    def __init__(self):
        """Create an instance of motor interface."""
        self.interface = MiniMotorDriver(left_channel, right_channel)

    def set_left_speed(self, speed, direction):
        """Set the speed of the left motors."""
        self._set_speed('left', speed, direction)

    def set_right_speed(self, speed, direction):
        """Set the speed of the right motor."""
        self._set_speed('right', speed, direction)

    def _set_speed(self, motor, speed, direction):
        if direction not in self.DIRECTIONS:
            LOGGER.error("Invalid direction %s", direction)
            return
        if speed > 100:
            LOGGER.warning("Capping speed %s to 100", speed)
        if speed < 0:
            LOGGER.warning("Applying floor to set speed %s to 0", speed)
        if motor == 'left':
            self.interface.setLeftMotor(direction, speed)
        else:
            self.interface.setRightMotor(direction, speed)

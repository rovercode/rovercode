"""Class for communicating with the GrovePi motor controller."""

import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))
try:
    import sys
    sys.path.append('../GrovePi/Software/Python')
    from grove_mini_motor_driver.grove_mini_motor_driver import MiniMotorDriver
except (ImportError, RuntimeError):
    LOGGER.warning("Grove I2C mini motor driver lib unavailable. Using dummy.")
    from drivers.dummy_grovepi_interface import MiniMotorDriver


class GroveMotors:
    """Helper functions for setting the GrovePi motor controllers."""

    DIRECTION_FORWARD = 'FORWARD'
    DIRECTION_BACKWARD = 'REVERSE'
    LEFT_DRIVER_ADDRESS = 0x60
    RIGHT_DRIVER_ADDRESS = 0x65
    DIRECTIONS = (DIRECTION_FORWARD, DIRECTION_BACKWARD)

    def __init__(self):
        """Create an instance of motor interface."""
        try:
            self.interface = MiniMotorDriver(self.LEFT_DRIVER_ADDRESS, self.RIGHT_DRIVER_ADDRESS)
        except RuntimeError:
            # MiniMotorDriver can fail based on hardware platform on init
            LOGGER.warning("Grove I2C mini motor driver lib unavailable. Using dummy.")
            from drivers.dummy_grovepi_interface import MiniMotorDriver as DummyMiniMotorDriver
            self.interface = DummyMiniMotorDriver(self.LEFT_DRIVER_ADDRESS, self.RIGHT_DRIVER_ADDRESS)
        self.interface.stopMotors()

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
            if speed == 0:
                self.interface.stopLeftMotor()
            else:
                self.interface.setLeftMotor(direction, speed)
        else:
            if speed == 0:
                self.interface.stopRightMotor()
            else:
                self.interface.setRightMotor(direction, speed)

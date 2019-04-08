"""Class for communicating with the GrovePi motor controller."""

import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))
try:
    from GrovePi.Software.Python.\
        grove_i2c_motor_driver.grove_i2c_motor_driver \
        import motor_driver
except ImportError:
    LOGGER.warn("GrovePi I2C motor driver lib unavailable. Using dummy.")
    from drivers.dummy_grovepi_interface import motor_driver


class GrovePiMotors:
    """Helper functions for setting the GrovePi motor controllers."""

    PORT_A = 'a'
    PORT_B = 'b'
    DIRECTION_FORWARD = 'forward'
    DIRECTION_BACKWARD = 'backward'

    def __init__(self):
        """Create an instance of motor interface."""
        self.interface = motor_driver()
        self.speeds = {self.PORT_A: 0, self.PORT_B: 0}
        self.directions = {self.PORT_A: 0, self.PORT_B: 0}

    def set_speed(self, port, speed, direction):
        """Set the speed of the motors."""
        port, direction = port.lower(), direction.lower()
        if self.speeds[port] == speed and self.directions[port] == direction:
            return
        self.speeds[port], self.directions[port] = speed, direction

        self.interface.MotorSpeedSetAB(self.speeds[self.PORT_A],
                                       self.speeds[self.PORT_B])

        direction_bits = \
            (self._direction_bits(self.directions[self.PORT_A]) << 2) + \
            (self._direction_bits(self.directions[self.PORT_B]))
        self.interface.DirectionSet(direction_bits)

    def _direction_bits(self, direction):
        return 0b10 if direction == self.DIRECTION_FORWARD else 0b01

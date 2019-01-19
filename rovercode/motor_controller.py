"""Class for managing the motor state."""

from constants import LEFT_MOTOR, RIGHT_MOTOR
import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))


class MotorController:
    """Object to manage the motor PWM states."""

    def __init__(self, left_forward_port, left_backward_port,
                 right_forward_port, right_backward_port, driver):
        """Construct a MotorManager."""
        self.ports = {}
        self.ports[LEFT_MOTOR] = {'forward': left_forward_port,
                                    'backward': left_backward_port}
        self.ports[RIGHT_MOTOR] = {'forward': right_forward_port,
                                     'backward': right_backward_port}
        self.driver = driver
        LOGGER.info("Motor manager initialized")

    def set_speed(self, motor, speed):
        """Set the speed of a motor pin."""
        LOGGER.info("Setting %s to %s", motor, speed)
        if speed > 0:
            ports = [self.ports[motor]['forward']]
        elif speed < 0:
            ports = [self.ports[motor]['backward']]
        else:
            ports = [self.ports[motor]['forward'],
                     self.ports[motor]['backward']]
        for port in ports:
            self.driver.set_speed(port, abs(speed))

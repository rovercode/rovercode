"""Class for managing the motor state."""

import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))
try:
    import Adafruit_GPIO.PWM as pwmLib
    import Adafruit_GPIO.GPIO as gpioLib
except ImportError:
    print LOGGER.warn("Adafruit_GPIO lib unavailable")


def singleton(class_):
    """Helper class for creating a singleton."""
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        else:
            print "Warning: tried to create multiple instances of singleton " + class_.__name__
        return instances[class_]
    return get_instance


@singleton
class AdafruitPwmManager:
    """Object to manage the motor PWM states."""

    DEFAULT_SOFTPWM_FREQ = 100
    ports = {}
    started_motors = []

    def __init__(self, left_forward_port, left_backward_port,
                 right_forward_port, right_backward_port):
        """Construct a MotorManager."""
        self.ports['left-motor'] = {'forward': left_forward_port, 'backward': left_backward_port}
        self.ports['right-motor'] = {'forward': right_forward_port, 'backward': right_backward_port}
        try:
            self.pwm = pwmLib.get_platform_pwm(pwmtype="softpwm")
        except NameError:
            LOGGER.warn("Adafruit_GPIO lib is unavailable")
        if self.pwm.__class__.__name__ == 'DUMMY_PWM_Adapter':
            def mock_set_duty_cycle(pin, speed):
                LOGGER.info("Starting pin %s at speed %s", pin, speed)
            self.pwm.set_duty_cycle = mock_set_duty_cycle

            def mock_start(pin, speed, frequency):
                LOGGER.info("Starting pin %s at speed %s and frequency %s", pin, speed, frequency)
            self.pwm.start = mock_start

        LOGGER.info("Motor manager started")

    def set_speed(self, motor, speed):
        """Set the speed of a motor pin."""
        LOGGER.info("Setting %s to %s", motor, speed)
        if speed > 0:
            ports = [self.ports[motor]['forward']]
        elif speed < 0:
            ports = [self.ports[motor]['backward']]
        else:
            ports = [self.ports[motor]['forward'], self.ports[motor]['backward']]
        for port in ports:
            if port in self.started_motors:
                self.pwm.set_duty_cycle(port, speed)
            else:
                self.pwm.start(port, speed, self.DEFAULT_SOFTPWM_FREQ)
                self.started_motors.append(port)




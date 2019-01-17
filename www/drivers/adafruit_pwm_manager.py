"""Class for managing the motor state."""

import logging
from singleton import Singleton
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))
try:
    import Adafruit_GPIO.PWM as pwmLib
    import Adafruit_GPIO.GPIO as gpioLib
except ImportError:
    print LOGGER.warn("Adafruit_GPIO lib unavailable")

@Singleton
class MotorManager:
    """Object to manage the motor PWM states."""

    DEFAULT_SOFTPWM_FREQ = 100
    started_motors = []

    def __init__(self):
        """Construct a MotorManager."""
        try:
            self.pwm = pwmLib.get_platform_pwm(pwmtype="softpwm")
        except NameError:
            LOGGER.warn("Adafruit_GPIO lib is unavailable")
        if self.pwm.__class__.__name__ == 'DUMMY_PWM_Adapter':
            def mock_set_duty_cycle(pin, speed):
                print "Setting pin " + pin + " to speed " + str(speed)
            self.pwm.set_duty_cycle = mock_set_duty_cycle

        LOGGER.info("Motor manager started")

    def set_speed(self, pin, speed):
        """Set the speed of a motor pin."""
        if pin in self.started_motors:
            self.pwm.set_duty_cycle(pin, speed)
        else:
            self.pwm.start(pin, speed, self.DEFAULT_SOFTPWM_FREQ)
            self.started_motors.append(pin)




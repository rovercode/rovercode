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
try:
    pwm = pwmLib.get_platform_pwm(pwmtype="softpwm")
    gpio = gpioLib.get_platform_gpio()
except NameError:
    LOGGER.warn("Adafruit_GPIO lib is unavailable")

@Singleton
class MotorManager:
    """Object to manage the motor PWM states."""

    DEFAULT_SOFTPWM_FREQ = 100
    started_motors = []

    def __init__(self):
        """Construct a MotorManager."""
        LOGGER.info("Motor manager started")
        if pwm.__class__.__name__ == 'DUMMY_PWM_Adapter':
            def mock_set_duty_cycle(pin, speed):
                print "Setting pin " + pin + " to speed " + str(speed)
            pwm.set_duty_cycle = mock_set_duty_cycle

    def set_speed(self, pin, speed):
        """Set the speed of a motor pin."""
        global pwm
        if pin in self.started_motors:
            pwm.set_duty_cycle(pin, speed)
        else:
            pwm.start(pin, speed, self.DEFAULT_SOFTPWM_FREQ)
            self.started_motors.append(pin)




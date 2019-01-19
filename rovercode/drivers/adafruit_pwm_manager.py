"""Class for managing the motor state."""

import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))
try:
    import Adafruit_GPIO.PWM as pwmLib
except ImportError:
    LOGGER.warn("Adafruit_GPIO lib unavailable")


class AdafruitPwmManager:
    """Object to manage the Adafruit PWM states."""

    DEFAULT_SOFTPWM_FREQ = 100
    started_motors = []

    def __init__(self):
        """Construct an Adafruit PWM manager."""
        try:
            self.pwm = pwmLib.get_platform_pwm(pwmtype="softpwm")
        except NameError:
            LOGGER.warn("Adafruit_GPIO lib is unavailable")
        if self.pwm.__class__.__name__ == 'DUMMY_PWM_Adapter':
            def mock_set_duty_cycle(pin, speed):
                LOGGER.info("Starting pin %s at speed %s", pin, speed)
            self.pwm.set_duty_cycle = mock_set_duty_cycle

            def mock_start(pin, speed, frequency):
                LOGGER.info("Starting pin %s at speed %s and frequency %s",
                            pin, speed, frequency)
            self.pwm.start = mock_start

        LOGGER.info("Adafruit PWM manager started")

    def set_speed(self, port, speed):
        """Set the speed of a motor pin."""
        if port in self.started_motors:
            self.pwm.set_duty_cycle(port, speed)
        else:
            self.pwm.start(port, speed, self.DEFAULT_SOFTPWM_FREQ)
            self.started_motors.append(port)

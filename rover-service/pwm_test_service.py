import Adafruit_GPIO.PWM as pwmLib
from time import time, sleep

#pwm = pwmLib.get_platform_pwm()
pwm = pwmLib.CHIP_PWM_Adapter()
pwm.start(5, 3, 1)
pwm.start(6, 15, 1)
sleep(3)
pwm.set_duty_cycle(5, 12)
pwm.set_frequency(5, 0.2)
sleep(10)
pwm.stop(5);
pwm.stop(6);

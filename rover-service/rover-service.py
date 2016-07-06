import Adafruit_GPIO.PWM as pwmLib
import Adafruit_GPIO.GPIO as gpioLib
import redis
import json

PWM_FREQ_HZ = 1000

r = redis.StrictRedis(host='localhost', port=6379, db=0)

pwm = pwmLib.get_platform_pwm(pwmtype="softpwm")
gpio = gpioLib.get_platform_gpio();

# Demonstrate overriding methods for debug if not on real hardware
if gpio.__class__.__name__ == 'DUMMYGPIOAdapter':
	def dummyGpioSetup(pin, mode, pull_up_down=gpioLib.PUD_OFF):
		print "Setting up dummy pin " + pin
	gpio.setup = dummyGpioSetup;

def leftEyeCallback(self):
	if gpio.is_high("XIO-P3"):
		event = 'leftEyeUncovered'
	else:
		event = 'leftEyeCovered'
	print event
	r.rpush('eventQueue', event);

def rightEyeCallback(self):
	if gpio.is_high("XIO-P4"):
		event = 'rightEyeUncovered'
	else:
		event = 'rightEyeCovered'
	print event
	r.rpush('eventQueue', event);

#Set up input listeners
gpio.setup("XIO-P3", gpioLib.IN)
gpio.add_event_detect("XIO-P3", gpioLib.BOTH, leftEyeCallback, 300)
gpio.setup("XIO-P4", gpioLib.IN)
gpio.add_event_detect("XIO-P4", gpioLib.BOTH, rightEyeCallback, 300)

while (True):
    rxd = r.lpop('commandQueue');
    if rxd:
        print rxd
        decoded = json.loads(rxd)
        print decoded['command']
        if decoded['command'] == 'START_MOTOR':
            print decoded['pin']
            print decoded['speed']
            print "Starting motor"
            pwm.start(decoded['pin'], float(decoded['speed']), PWM_FREQ_HZ)
        elif decoded['command'] == 'STOP_MOTOR':
            print decoded['pin']
            print "Stopping motor"
            pwm.stop(decoded['pin'])
		elif decoded['command'] == 'GET_SENSOR_VAL_BOOL':
			print decoded

pwm.cleanup()

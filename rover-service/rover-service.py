import Adafruit_GPIO.PWM as pwmLib
import Adafruit_GPIO.GPIO as gpioLib
import redis
import json
import threading

PWM_FREQ_HZ = 1000

r = redis.StrictRedis(host='localhost', port=6379, db=0)

# pwm = pwmLib.get_platform_pwm(pwmtype="softpwm")
gpio = gpioLib.get_platform_gpio();

# Demonstrate overriding methods for debug if not on real hardware
if gpio.__class__.__name__ == 'DUMMYGPIOAdapter':
	def dummyGpioSetup(pin, mode, pull_up_down=gpioLib.PUD_OFF):
		print "Setting up dummy pin " + pin
	gpio.setup = dummyGpioSetup;

killThreadsFlag = False;

#Sometimes sensor edges are so slow that polling is best
class gpioPoller (threading.Thread):
	def __init__(self, threadID, name, pin, risingEvent, fallingEvent):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.pin = pin
		self.risingEvent = risingEvent
		self.fallingEvent = fallingEvent

	def run(self):
		oldVal = True;
		while (not killThreadsFlag):
			newVal = gpio.is_high(self.pin)
			if (oldVal == False) and (newVal == True):
				print self.risingEvent
				r.rpush('eventQueue', self.risingEvent)
			elif (oldVal == True) and (newVal == False):
				print self.fallingEvent
				r.rpush('eventQueue', self.fallingEvent)
			else:
				pass
			oldVal = newVal
		self.name.exit()

# set up IR sensor gpio
gpio.setup("XIO-P2", gpioLib.IN)
gpio.setup("XIO-P4", gpioLib.IN)
rightEyePollingThread = gpioPoller(1, "rightEyePollingThread", "XIO-P4", 'rightEyeUncovered', 'rightEyeCovered')
rightEyePollingThread.start();
leftEyePollingThread = gpioPoller(2, "leftEyePollingThread", "XIO-P2", 'leftEyeUncovered', 'leftEyeCovered')
leftEyePollingThread.start();

# set up motor gpio
# pwm.start("XIO-P0", 0);
# pwm.start("XIO-P1", 0);
# pwm.start("XIO-P6", 0);
# pwm.start("XIO-P7", 0);


# while (True):
#     rxd = r.lpop('commandQueue');
#     if rxd:
#         print rxd
#         decoded = json.loads(rxd)
#         print decoded['command']
#         if decoded['command'] == 'START_MOTOR':
#             print decoded['pin']
#             print decoded['speed']
#             print "Starting motor"
#             pwm.set_duty_cycle(decoded['pin'], float(decoded['speed']))
#         elif decoded['command'] == 'STOP_MOTOR':
#             print decoded['pin']
#             print "Stopping motor"
#             pwm.set_duty_cycle(decoded['pin'], 0)
killThreadsFlag = True;
gpioLib.cleanup();
pwm.cleanup()

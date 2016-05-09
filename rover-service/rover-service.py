import Adafruit_GPIO.PWM as pwmLib
import redis
import json

PWM_FREQ_HZ = 1000

r = redis.StrictRedis(host='localhost', port=6379, db=0)

pwm = pwmLib.get_platform_pwm(2)

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

pwm.cleanup()

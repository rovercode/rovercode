import Adafruit_GPIO.PWM as pwmLib
import redis
import json

PWM_FREQ_HZ = 20

r = redis.StrictRedis(host='localhost', port=6379, db=0)

#pwm = pwmLib.get_platform_pwm()
pwm = pwmLib.CHIP_PWM_Adapter()

while True:
    rxd = r.blpop('motorQueue', 0)
    decoded = json.loads(rxd[1])
    print decoded['command']
    print decoded['pin']
    print decoded['speed']
    print decoded['direction']
    if decoded['command'] == 'START':
        pwm.start(decoded['pin'], decoded['speed'], PWM_FREQ_HZ)
    elif decoded['command'] == 'STOP':
        pwm.stop(decoded['pin'])

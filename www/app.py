from flask import Flask, jsonify, Response, request
from os import listdir
from os.path import isfile, join
from flask_cors import CORS, cross_origin
import xml.etree.ElementTree
import Adafruit_GPIO.PWM as pwmLib
import Adafruit_GPIO.GPIO as gpioLib
import json
import threading

app = Flask(__name__)
CORS(app)

PWM_FREQ_HZ = 1000

pwm = pwmLib.get_platform_pwm(pwmtype="softpwm")
gpio = gpioLib.get_platform_gpio();


@app.route('/api/v1/blockdiagrams', methods=['GET'])
def getblockdiagrams():
    names = []
    for f in listdir('saved-bds'):
        if isfile(join('saved-bds', f)) and f.endswith('.xml'):
            names.append(xml.etree.ElementTree.parse(join('saved-bds', f)).getroot().find('designName').text)
    return jsonify(result=names)

@app.route('/api/v1/blockdiagrams', methods=['POST'])
def saveblockdiagram():
    designName = request.form['designName'].replace(' ', '_').replace('.', '_')
    bdString = request.form['bdString']
    root = xml.etree.ElementTree.Element("root")

    xml.etree.ElementTree.SubElement(root, 'designName').text = designName
    xml.etree.ElementTree.SubElement(root, 'bd').text = bdString

    tree = xml.etree.ElementTree.ElementTree(root)
    tree.write('saved-bds/' + designName + '.xml')
    return ('', 200)

@app.route('/api/v1/blockdiagrams/<string:id>', methods=['GET'])
def getblockdiagram(id):
    id = id.replace(' ', '_').replace('.', '_')
    bd = [f for f in listdir('saved-bds') if isfile(join('saved-bds', f)) and id in f]
    with open(join('saved-bds',bd[0]), 'r') as content_file:
        content = content_file.read()
    return Response(content, mimetype='text/xml')

@app.route('/api/v1/sendcommand', methods = ['POST'])
def sendCommand():
    runCommand(request.json)
    return jsonify(request.json)

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
        
def init_rover_service():
    # Demonstrate overriding methods for debug if not on real hardware
    if gpio.__class__.__name__ == 'DUMMYGPIOAdapter':
	    def dummyGpioSetup(pin, mode, pull_up_down=gpioLib.PUD_OFF):
		    print "Setting up dummy pin " + pin
	    gpio.setup = dummyGpioSetup;

    killThreadsFlag = False;

    # set up IR sensor gpio
    gpio.setup("XIO-P2", gpioLib.IN)
    gpio.setup("XIO-P4", gpioLib.IN)
    #rightEyePollingThread = gpioPoller(1, "rightEyePollingThread", "XIO-P4", 'rightEyeUncovered', 'rightEyeCovered')
    #rightEyePollingThread.start();
    #leftEyePollingThread = gpioPoller(2, "leftEyePollingThread", "XIO-P2", 'leftEyeUncovered', 'leftEyeCovered')
    #leftEyePollingThread.start();

    # set up motor gpio
    pwm.start("XIO-P0", 0);
    pwm.start("XIO-P1", 0);
    pwm.start("XIO-P6", 0);
    pwm.start("XIO-P7", 0);

    if pwm.__class__.__name__ == 'DUMMY_PWM_Adapter':
        def mock_set_duty_cycle(pin, speed):
            print "Setting pin " + pin + " to speed " + str(speed)
        pwm.set_duty_cycle = mock_set_duty_cycle

def runCommand(decoded):
    print decoded['command']
    if decoded['command'] == 'START_MOTOR':
        print decoded['pin']
        print decoded['speed']
        print "Starting motor"
        pwm.set_duty_cycle(decoded['pin'], float(decoded['speed']))
    elif decoded['command'] == 'STOP_MOTOR':
        print decoded['pin']
        print "Stopping motor"
        pwm.set_duty_cycle(decoded['pin'], 0)

if __name__ == '__main__':
    init_rover_service()
    app.run(host='0.0.0.0', debug=True)


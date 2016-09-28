from flask import Flask, jsonify, Response, request
from os import listdir
from os.path import isfile, join
from flask_cors import CORS, cross_origin
import xml.etree.ElementTree
import Adafruit_GPIO.PWM as pwmLib

app = Flask(__name__)
CORS(app)

pwm = pwmLib.get_platform_pwm(pwmtype="softpwm")

@app.route('/api/v1/blockdiagrams', methods=['GET'])
def get_block_diagrams():
    names = []
    for f in listdir('saved-bds'):
        if isfile(join('saved-bds', f)) and f.endswith('.xml'):
            names.append(xml.etree.ElementTree.parse(join('saved-bds', f)).getroot().find('designName').text)
    return jsonify(result=names)

@app.route('/api/v1/blockdiagrams', methods=['POST'])
def save_block_diagram():
    designName = request.form['designName'].replace(' ', '_').replace('.', '_')
    bdString = request.form['bdString']
    root = xml.etree.ElementTree.Element("root")

    xml.etree.ElementTree.SubElement(root, 'designName').text = designName
    xml.etree.ElementTree.SubElement(root, 'bd').text = bdString

    tree = xml.etree.ElementTree.ElementTree(root)
    tree.write('saved-bds/' + designName + '.xml')
    return ('', 200)

@app.route('/api/v1/blockdiagrams/<string:id>', methods=['GET'])
def get_block_diagram(id):
    id = id.replace(' ', '_').replace('.', '_')
    bd = [f for f in listdir('saved-bds') if isfile(join('saved-bds', f)) and id in f]
    with open(join('saved-bds',bd[0]), 'r') as content_file:
        content = content_file.read()
    return Response(content, mimetype='text/xml')

@app.route('/api/v1/sendcommand', methods = ['POST'])
def send_command():
    run_command(request.json)
    return jsonify(request.json) 

def init_rover_service():
    # set up motor pwm
    pwm.start("XIO-P0", 0);
    pwm.start("XIO-P1", 0);
    pwm.start("XIO-P6", 0);
    pwm.start("XIO-P7", 0);

    # test adapter
    if pwm.__class__.__name__ == 'DUMMY_PWM_Adapter':
        def mock_set_duty_cycle(pin, speed):
            print "Setting pin " + pin + " to speed " + str(speed)
        pwm.set_duty_cycle = mock_set_duty_cycle

def run_command(decoded):
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

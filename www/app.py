"""Rovercode app."""
import websocket
import thread
import logging
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import json, socket
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))

from drivers.VCNL4010 import VCNL4010
from drivers.DummyBinarySensor import DummyBinarySensor
from drivers.adafruit_pwm_manager import AdafruitPwmManager
from binary_sensor import BinarySensor

"""Globals"""
adafruit_motor_manager = None
ROVERCODE_WEB_REG_URL = ''
ROVERCODE_WEB_OAUTH2_URL = ''
ws_thread = None
hb_thread = None


"""Create flask app"""
app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": [".*rovercode.com", ".*localhost"]}})

def get_local_ip():
    """Get the local area network IP address of the rover."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def connect():
    """Connect to the rovercode-web websocket."""
    global ws_thread
    print 'Websocket connected'
    if ws_thread is None:
        ws_thread = socketio.start_background_task(target=sensors_thread)
    emit('status', {'data': 'Connected'})

def test_message(message):
    """Send a debug test message when status is received from rovercode-web."""
    print "Got a status message: " + message['data']

@app.route('/', methods = ['GET'])
def display_home_message():
    """Display a message if someone points a browser at the root."""
    return ("The rover is running its service at this address.")

@app.route('/api/v1/sendcommand', methods = ['POST'])
def send_command():
    """
    API: /sendcommand [POST].

    Executes the posted command

    **Available Commands:**::
        START_MOTOR
        STOP_MOTOR
    """
    run_command(request.form)
    return jsonify(request.form)


def init_inputs(rover_params, dummy=False):
    """Initialize input GPIO."""
    binary_sensors = []

    def get_env_int(name):
        try:
            return int(os.getenv(name, None))
        except Exception:
            return None

    left_eye_led_current = get_env_int('LEFT_EYE_LED_CURRENT')
    left_eye_threshold = get_env_int('LEFT_EYE_THRESHOLD')
    right_eye_led_current = get_env_int('RIGHT_EYE_LED_CURRENT')
    right_eye_threshold = get_env_int('RIGHT_EYE_THRESHOLD')
    if not dummy:
        binary_sensors.append(BinarySensor(
            "left_ir_sensor",
            VCNL4010(rover_params['left_eye_I2C_port'], rover_params['left_eye_i2c_addr'], left_eye_led_current, left_eye_threshold)))
        binary_sensors.append(BinarySensor(
            "right_ir_sensor",
            VCNL4010(rover_params['right_eye_port'], rover_params['right_eye_addr'], right_eye_led_current, right_eye_threshold)))
    else:
        binary_sensors.append(BinarySensor("left_dummy_sensor", DummyBinarySensor()))
        binary_sensors.append(BinarySensor("right_dummy_sensor",DummyBinarySensor()))

    return binary_sensors


def run_command(decoded):
    """
    Run the command specified by `decoded`.

    :param decoded:
        The command to run
    """
    print decoded['command']
    global adafruit_motor_manager
    if decoded['command'] == 'START_MOTOR':
        print decoded['pin']
        print decoded['speed']
        print "Starting motor"
        adafruit_motor_manager.set_speed(decoded['pin'], float(decoded['speed']))
    elif decoded['command'] == 'STOP_MOTOR':
        print decoded['pin']
        print "Stopping motor"
        adafruit_motor_manager.set_speed(decoded['pin'], 0)


def on_message(ws, raw_message):
    global adafruit_motor_manager
    message = json.loads(raw_message)
    type = message['type']
    if type == 'motor-command':
        adafruit_motor_manager.set_speed(message['motor-id'], message['motor-value'])


def on_error(ws, error):
    LOGGER.error(error)


def on_close(ws):
    LOGGER.warn("Websocket connection closed")


def on_open(ws):
    def send_heartbeat(*args):
        """Send a periodic message to the websocket server."""
        while True:
            time.sleep(3)
            ws.send(json.dumps({"type": "heartbeat"}))

    def poll_sensors(binary_sensors):
        """Scan each binary sensor and sends events based on changes."""
        while True:
            time.sleep(0.2)
            sensor_message = {
                "type": "sensor-reading",
                "sensor-type": "binary",
                "unit": "active-high"
            }
            for sensor in binary_sensors:
                time.sleep(0.2)
                sensor_message['sensor-id'] = sensor.name
                changed_value = sensor.get_change()
                if changed_value is not None:
                    sensor_message['sensor-value'] = changed_value
                    ws.send(json.dumps(sensor_message))

    info = json.loads(session.get('{}/api/v1/rovers?client_id={}'.format(rovercode_web_url, client_id)).text)[0]
    LOGGER.info("Found myself - I am %s, with id %s", info['name'], info['id'])

    # Create motor manager
    global adafruit_motor_manager
    adafruit_motor_manager = AdafruitPwmManager(info['left_forward_pin'], info['left_backward_pin'],
                                                info['right_forward_pin'], info['right_backward_pin'])

    # Start heartbeat thread
    thread.start_new_thread(send_heartbeat, ())
    LOGGER.info("Heartbeat thread started")

    # Start inputs thread
    binary_sensors = init_inputs(info, dummy='rovercode.com' not in rovercode_web_host)
    thread.start_new_thread(poll_sensors, (binary_sensors,))
    LOGGER.info("Sensors thread started")


if __name__ == '__main__':
    LOGGER.info("Starting the Rovercode service!")
    load_dotenv('../.env')
    rovercode_web_host = os.getenv("ROVERCODE_WEB_HOST", "rovercode.com")

    rovercode_web_host_secure = os.getenv("ROVERCODE_WEB_HOST_SECURE", 'True').lower() == 'true'
    if rovercode_web_host[-1:] == '/':
        rovercode_web_host = rovercode_web_host[:-1]
    rovercode_web_url = "{}://{}".format("https" if rovercode_web_host_secure else "http", rovercode_web_host)

    client_id = os.getenv('CLIENT_ID', '')
    if client_id == '':
        raise NameError("Please add CLIENT_ID to your .env")
    client_secret = os.getenv('CLIENT_SECRET', '')
    if client_secret == '':
        raise NameError("Please add CLIENT_SECRET to your .env")

    LOGGER.info("Targeting host %s. My client id is %s", rovercode_web_url, client_id)

    if not rovercode_web_host_secure:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    client = BackendApplicationClient(client_id=client_id)
    session = OAuth2Session(client=client)
    session.fetch_token(token_url='{}/oauth2/token/'.format(rovercode_web_url),
                        client_id=client_id,
                        client_secret=client_secret)

    ws_url = "{}://{}/ws/realtime/{}/".format("wss" if rovercode_web_host_secure else "ws", rovercode_web_host, client_id)
    auth_string = "Authorization: Bearer {}".format(session.access_token)
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close, header=[auth_string])
    ws.on_open = on_open
    ws.run_forever()



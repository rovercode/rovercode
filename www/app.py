"""Rovercode app."""
import websocket
import thread
import logging
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests, json, socket
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv, find_dotenv
import os

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))

try:
    import Adafruit_GPIO.PWM as pwmLib
    import Adafruit_GPIO.GPIO as gpioLib
except ImportError:
    print LOGGER.warn("Adafruit_GPIO lib unavailable")

from drivers.VCNL4010 import VCNL4010
from drivers.DummyBinarySensor import DummyBinarySensor

"""Globals"""
ROVERCODE_WEB_REG_URL = ''
ROVERCODE_WEB_OAUTH2_URL = ''
DEFAULT_SOFTPWM_FREQ = 100
binary_sensors = []
ws_thread = None
hb_thread = None

try:
    pwm = pwmLib.get_platform_pwm(pwmtype="softpwm")
    gpio = gpioLib.get_platform_gpio()
except NameError:
    LOGGER.warn("Adafruit_GPIO lib is unavailable")

"""Create flask app"""
app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": [".*rovercode.com", ".*localhost"]}})

class BinarySensor:
    """
    The binary sensor object contains information for each binary sensor.

    :param name:
        The human readable name of the sensor
    :param sensor:
        The object representing the hardware sensor
    """

    def __init__(self, name, sensor):
        """Constructor for BinarySensor object."""
        self.name = name
        self.sensor = sensor
        self.old_val = False

def get_local_ip():
    """Get the local area network IP address of the rover."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

class HeartBeatManager():
    """
    A manager to register the rover with rovercode-web and periodically check in.

    :param client_id:
        The Oauth2 client id for this rover.
    :param client_secret:
        The Oauth2 client secret for this rover.
    """

    def __init__(self, client_id, client_secret, id=None):
        """Constructor for the HeartBeatManager."""
        self.run = True
        self.thread = None
        self.web_id = id
        self.client_id = client_id
        self.name = None
        self.local_ip = get_local_ip()
        self.auth_header = None

        # Log in to rovercode-web using oauth credentials
        login_data = {
            'grant_type':'client_credentials',
            'client_id':client_id,
            'client_secret':client_secret,
        }
        r = requests.post(ROVERCODE_WEB_OAUTH2_URL + '/', data=login_data)
        self.access_token = r.json()['access_token']
        self.auth_header = {'Authorization':'Bearer ' + self.access_token}

    def update(self):
        """Check in with rovercode-web, updating our timestamp."""
        payload = {'name': self.name, 'local_ip': self.local_ip}
        return requests.put(ROVERCODE_WEB_REG_URL+"/"+str(self.web_id)+"/",
                                data=payload,
                                headers=self.auth_header)

    def read(self):
        """Look for our name on rovercode-web. Sets web_id if found."""
        result = requests.get(ROVERCODE_WEB_REG_URL+'?client_id='+self.client_id, headers=self.auth_header)
        try:
            info = json.loads(result.text)[0]
            self.web_id = info['id']
            self.name = info['name']
            init_inputs(
                info['left_eye_i2c_port'],
                info['left_eye_i2c_addr'],
                info['right_eye_i2c_port'],
                info['right_eye_i2c_addr']
            )
        except (KeyError, IndexError) as e:
            LOGGER.error("Missing something important from rover payload: %s", e)
            self.web_id = None

    def stopThread(self):
        """Gracefully stop the periodic check-in thread."""
        self.run = False

    def thread_func(self, run_once=False):
        """Thread function that periodically checks in with rovercode-web."""
        self.read()
        while self.run:
            if self.web_id is not None:
                print "Checking in with rovercode-web with ID " + str(self.web_id)
                r = self.update()
                if r.status_code in [200, 201]:
                    print "... success"
                else:
                    print "... error while updating"
            else:
                print "No rover web-id found when trying to update!"
            if run_once:
                break
            time.sleep(3)
        print "Exiting heartbeat thread"
        return



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
    global binary_sensors

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
        binary_sensors.append(BinarySensor(
            "left_dummy_sensor",
            DummyBinarySensor()
        ))
        binary_sensors.append(BinarySensor(
            "right_dummy_sensor",
            DummyBinarySensor()
        ))

    # test adapter
    if pwm.__class__.__name__ == 'DUMMY_PWM_Adapter':
        def mock_set_duty_cycle(pin, speed):
            print "Setting pin " + pin + " to speed " + str(speed)
        pwm.set_duty_cycle = mock_set_duty_cycle

def singleton(class_):
    """Helper class for creating a singleton."""
    instances = {}
    def getInstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        else:
            print "Warning: tried to create multiple instances of singleton " + class_.__name__
        return instances[class_]
    return getInstance

@singleton
class MotorManager:
    """Object to manage the motor PWM states."""

    started_motors = []

    def __init__(self):
        """Contruct a MotorManager."""
        LOGGER.info("Starting motor manager")

    def set_speed(self, pin, speed):
        """Set the speed of a motor pin."""
        global pwm
        if pin in self.started_motors:
            pwm.set_duty_cycle(pin, speed)
        else:
            pwm.start(pin, speed, DEFAULT_SOFTPWM_FREQ)
            self.started_motors.append(pin)

def run_command(decoded):
    """
    Run the command specified by `decoded`.

    :param decoded:
        The command to run
    """
    print decoded['command']
    global motor_manager
    if decoded['command'] == 'START_MOTOR':
        print decoded['pin']
        print decoded['speed']
        print "Starting motor"
        motor_manager.set_speed(decoded['pin'], float(decoded['speed']))
    elif decoded['command'] == 'STOP_MOTOR':
        print decoded['pin']
        print "Stopping motor"
        motor_manager.set_speed(decoded['pin'], 0)

def set_rovercodeweb_url(base_url):
    """Set the global URL variables for rovercodeweb."""
    global ROVERCODE_WEB_OAUTH2_URL
    global ROVERCODE_WEB_REG_URL
    ROVERCODE_WEB_REG_URL = base_url + "api/v1/rovers"
    ROVERCODE_WEB_OAUTH2_URL = base_url + "oauth2/token"


def on_message(ws, message):
    LOGGER.info(message)


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

    def poll_sensors(*args):
        """Scan each binary sensor and sends events based on changes."""
        while True:
            sensor_message = {
                "type": "sensor-reading",
                "sensor-type": "binary",
                "sensor-id": None,
                "sensor-value": None,
                "unit": "active-high"
            }
            global binary_sensors
            for s in binary_sensors:
                time.sleep(0.4)
                sensor_message['sensor-id'] = s.name
                try:
                    new_val = s.sensor.is_high()
                except IOError:
                    # Skip it and try again later
                    continue
                if not s.old_val and new_val:
                    sensor_message['sensor-value'] = True
                    ws.send(json.dumps(sensor_message))
                elif s.old_val and not new_val:
                    sensor_message['sensor-value'] = False
                    ws.send(json.dumps(sensor_message))
                else:
                    pass
                s.old_val = new_val

    thread.start_new_thread(send_heartbeat, ())
    LOGGER.info("Heartbeat thread started")

    thread.start_new_thread(poll_sensors, ())
    LOGGER.info("Sensors thread started")


if __name__ == '__main__':
    LOGGER.info("Starting the Rovercode service!")
    load_dotenv('../.env')
    rovercode_web_host = os.getenv("ROVERCODE_WEB_HOST", "rovercode.com")

    rovercode_web_host_secure = os.getenv("ROVERCODE_WEB_HOST_SECURE", 'True').lower() == 'true'
    if rovercode_web_host[-1:] == '/':
        rovercode_web_host = rovercode_web_host[:-1]
    rovercode_web_url = "{}://{}".format("https" if rovercode_web_host_secure else "http", rovercode_web_host)
    set_rovercodeweb_url(rovercode_web_url)

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

    info = json.loads(session.get('{}/api/v1/rovers?client_id={}'.format(rovercode_web_url, client_id)).text)[0]
    LOGGER.info("Found myself - I am %s, with id %s", info['name'], info['id'])
    init_inputs(info, dummy='rovercode.com' not in rovercode_web_host)

    motor_manager = MotorManager()

    ws_url = "{}://{}/ws/realtime/{}/".format("wss" if rovercode_web_host_secure else "ws", rovercode_web_host, client_id)
    auth_string = "Authorization: Bearer {}".format(session.access_token)
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close, header=[auth_string])
    ws.on_open = on_open
    ws.run_forever()



"""Rovercode app."""
import websocket
from threading import Thread
import logging
import time
import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))

from drivers.binary_sensor import BinarySensor
from drivers.dummy_binary_sensor import DummyBinarySensor
from drivers.adafruit_pwm_manager import AdafruitPwmManager
from drivers.VCNL4010 import VCNL4010

"""Globals"""
adafruit_motor_manager = None


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
    t = Thread(target=send_heartbeat)
    t.start()
    LOGGER.info("Heartbeat thread started")

    # Start inputs thread
    binary_sensors = init_inputs(info, dummy='rovercode.com' not in rovercode_web_host)
    t = Thread(target=poll_sensors, args=(binary_sensors,))
    t.start()
    LOGGER.info("Sensors thread started")


if __name__ == '__main__':
    LOGGER.info("Starting the Rovercode service!!!!")
    load_dotenv('.env')
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



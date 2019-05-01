"""Rovercode app."""
from threading import Thread
import logging
import time
import json
import os

from dotenv import load_dotenv
import websocket
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

import constants
from motor_controller import MotorController
from drivers.grove_motors import GroveMotors
from input_utils import init_inputs

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))


def send_heartbeat(ws, run_once_only=False):
    """Send a periodic message to the websocket server."""
    while True:
        ws.send(json.dumps({constants.MESSAGE_TYPE: constants.HEARTBEAT_TYPE}))
        if run_once_only:
            break
        time.sleep(3)  # pragma: no cover


def poll_sensors(ws, binary_sensors, run_once_only=False):
    """Scan each binary sensor and send events based on changes."""
    while True:
        sensor_message = {
            constants.MESSAGE_TYPE: constants.SENSOR_READING_TYPE,
            constants.SENSOR_TYPE_FIELD: constants.SENSOR_TYPE_BINARY,
            constants.UNIT_FIELD: constants.SENSOR_UNIT_ACTIVE_HIGH
        }
        for sensor in binary_sensors:
            time.sleep(0.2)
            sensor_message[constants.SENSOR_ID_FIELD] = sensor.name
            changed_value = sensor.get_change()
            if changed_value is not None:
                sensor_message[constants.SENSOR_VALUE_FIELD] = changed_value
                ws.send(json.dumps(sensor_message))
        if run_once_only:
            break
        time.sleep(0.2)  # pragma: no cover


def on_message(ws, raw_message):
    """Handle incoming websocket message."""
    global motor_controller
    message = json.loads(raw_message)
    type = message[constants.MESSAGE_TYPE]
    if type == constants.MOTOR_COMMAND:
        if (message[constants.MOTOR_ID_FIELD] not in constants.MOTOR_IDS):
            LOGGER.warning(
                "Invalid motor {}".format(message[constants.MOTOR_ID_FIELD]))
            return
        motor_controller.set_speed(message[constants.MOTOR_ID_FIELD],
                                   message[constants.MOTOR_VALUE_FIELD],
                                   message[constants.MOTOR_DIRECTION_FIELD])


def on_error(ws, error):  # pragma: no cover
    """Handle error from websocket connection."""
    LOGGER.error(error)


def on_close(ws):  # pragma: no cover
    """Handle closing of websocket connection."""
    LOGGER.warning("Websocket connection closed")


def on_open(ws):
    """Start up threads upon opening websocket connections."""
    global session
    global motor_controller
    global rovercode_web_url
    global client_id

    info = json.loads(session.get('{}/api/v1/rovers?client_id={}'.format(rovercode_web_url, client_id)).text)['results'][0]
    LOGGER.info("Found myself - I am %s, with id %s", info[constants.ROVER_NAME], info[constants.ROVER_ID])
    rover_config = info[constants.ROVER_CONFIG]

    # Create motor manager
    left_motor_port, right_motor_port =\
        rover_config.get(constants.LEFT_MOTOR_PORT), rover_config.get(constants.RIGHT_MOTOR_PORT)
    if any((left_motor_port is None, right_motor_port is None)):
        raise ValueError('Required motor port configuration not present in Rover config')
    motor_controller = MotorController(left_motor_port, right_motor_port, GroveMotors())

    # Start heartbeat thread
    t = Thread(target=send_heartbeat, args=(ws,))
    t.start()
    LOGGER.info("Heartbeat thread started")

    # Start inputs thread
    binary_sensors = init_inputs(rover_config)
    t = Thread(target=poll_sensors, args=(ws, binary_sensors))
    t.start()
    LOGGER.info("Sensors thread started")


def run_service(run_forever=True, use_dotenv=True):
    """Kick off the service."""
    global session
    global motor_controller
    global rovercode_web_url
    global client_id
    LOGGER.info("Starting the Rovercode service!")
    if use_dotenv:  # pragma: no cover
        load_dotenv('../.env')
    rovercode_web_host = os.getenv("ROVERCODE_WEB_HOST", "rovercode.com")

    rovercode_web_host_secure = os.getenv("ROVERCODE_WEB_HOST_SECURE", 'True').lower() == 'true'
    if rovercode_web_host[-1:] == '/':  # pragma: no cover
        rovercode_web_host = rovercode_web_host[:-1]
    rovercode_web_url = "{}://{}".format("https" if rovercode_web_host_secure else "http", rovercode_web_host)

    client_id = os.getenv('CLIENT_ID', '')
    if client_id == '':  # pragma: no cover
        raise NameError("Please add CLIENT_ID to your .env")
    client_secret = os.getenv('CLIENT_SECRET', '')
    if client_secret == '':  # pragma: no cover
        raise NameError("Please add CLIENT_SECRET to your .env")

    LOGGER.info("Targeting host %s. My client id is %s", rovercode_web_url, client_id)

    if not rovercode_web_host_secure:  # pragma: no cover
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    client = BackendApplicationClient(client_id=client_id)
    global session
    session = OAuth2Session(client=client)
    session.fetch_token(token_url='{}/oauth2/token/'.format(rovercode_web_url),
                        client_id=client_id,
                        client_secret=client_secret)

    ws_url = "{}://{}/ws/realtime/{}/".format("wss" if rovercode_web_host_secure else "ws", rovercode_web_host, client_id)
    auth_string = "Authorization: Bearer {}".format(session.access_token)
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close, header=[auth_string])
    ws.on_open = on_open
    if run_forever:  # pragma: no cover
        ws.run_forever()


if __name__ == '__main__':  # pragma: no cover
    run_service()



"""Rovercode app."""
from threading import Thread
import logging
import time
import json
import os
import functools
from multiprocessing import SimpleQueue

from dotenv import load_dotenv
from websocket import WebSocketApp
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

import constants
from motor_controller import MotorController
from chainable_rgb_leds_manager import ChainableRgbLedsManager
from drivers.grove_motors import GroveMotors
from drivers.grovepi_chainable_rgb_leds import GrovePiChainableRgbLeds
from input_utils import init_inputs

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))

# Globals
ROVERCODE_WEB_URL = None
ROVER_CONFIG = None
MOTOR_CONTROLLER = None
CHAINABLE_RGB_MANAGER = None
CLIENT_ID = None
SESSION = None
GROVEPI_QUEUE = SimpleQueue()


def send_heartbeat(ws_connection, run_once_only=False):
    """Send a periodic message to the websocket server."""
    while True:
        ws_connection.send(json.dumps(
            {constants.MESSAGE_TYPE: constants.HEARTBEAT_TYPE}))
        if run_once_only:
            break
        time.sleep(3)  # pragma: no cover


def grovepi_thread_loop(ws_connection, binary_sensors, run_once_only=False):
    """Scan each binary sensor and send events based on changes."""
    global GROVEPI_QUEUE

    while True:
        # Handle queued actions
        if not GROVEPI_QUEUE.empty():
            # Perform one action per loop
            action = GROVEPI_QUEUE.get()
            try:
                action()
            except ValueError as exception:
                LOGGER.error(f'Unable to perform GrovePi action: {exception}')

        # Read sensors
        sensor_message = {
            constants.MESSAGE_TYPE: constants.SENSOR_READING_TYPE,
            constants.SENSOR_TYPE_FIELD: constants.SENSOR_TYPE_BINARY,
            constants.UNIT_FIELD: constants.SENSOR_UNIT_ACTIVE_HIGH
        }
        for sensor in binary_sensors:
            time.sleep(0.05)
            sensor_message[constants.SENSOR_ID_FIELD] = sensor.name
            changed_value = sensor.get_change()
            if changed_value is not None:
                sensor_message[constants.SENSOR_VALUE_FIELD] = changed_value
                ws_connection.send(json.dumps(sensor_message))
        if run_once_only:
            break


def on_message(_, raw_message):
    """Handle incoming websocket message."""
    global MOTOR_CONTROLLER
    global CHAINABLE_RGB_MANAGER
    global GROVEPI_QUEUE
    message = json.loads(raw_message)
    message_type = message[constants.MESSAGE_TYPE]
    if message_type == constants.MOTOR_COMMAND:
        if message[constants.MOTOR_ID_FIELD] not in constants.MOTOR_IDS:
            LOGGER.warning("Invalid motor %s",
                           message[constants.MOTOR_ID_FIELD])
            return
        MOTOR_CONTROLLER.set_speed(message[constants.MOTOR_ID_FIELD],
                                   message[constants.MOTOR_VALUE_FIELD],
                                   message[constants.MOTOR_DIRECTION_FIELD])
    elif message_type == constants.CHAINABLE_RGB_LED_COMMAND:
        led_id = message.get(constants.CHAINABLE_RGB_LED_ID_FIELD)
        LOGGER.info(f'Queueing RGB LED command to LED {led_id}')
        GROVEPI_QUEUE.put(
            functools.partial(
                CHAINABLE_RGB_MANAGER.set_led_color, led_id,
                message.get(constants.CHAINABLE_RGB_LED_RED_VALUE_FIELD),
                message.get(constants.CHAINABLE_RGB_LED_GREEN_VALUE_FIELD),
                message.get(constants.CHAINABLE_RGB_LED_BLUE_VALUE_FIELD)
            )
        )


def on_error(_, error):  # pragma: no cover
    """Handle error from websocket connection."""
    LOGGER.error(error)


def on_close(_):  # pragma: no cover
    """Handle closing of websocket connection."""
    LOGGER.warning("Websocket connection closed")


def on_open(ws_connection):
    """Start up threads upon opening websocket connections."""
    global CHAINABLE_RGB_MANAGER
    global ROVER_CONFIG
    global GROVEPI_QUEUE

    # Start heartbeat thread
    thread = Thread(target=send_heartbeat, args=(ws_connection,))
    thread.start()
    LOGGER.info("Heartbeat thread started")

    # Start inputs thread
    binary_sensors = init_inputs(ROVER_CONFIG)
    thread = Thread(target=grovepi_thread_loop,
                    args=(ws_connection, binary_sensors))
    thread.start()
    LOGGER.info("GrovePi thread started")

    # Set LEDs to "OK" blue
    GROVEPI_QUEUE.put(
        functools.partial(
            CHAINABLE_RGB_MANAGER.set_all_led_colors, *constants.RGB_BLUE
        )
    )


def _get_web_url():
    web_host = os.getenv("ROVERCODE_WEB_HOST", "app.rovercode.com")
    web_host_secure = \
        os.getenv("ROVERCODE_WEB_HOST_SECURE", 'True').lower() == 'true'
    if web_host[-1:] == '/':  # pragma: no cover
        web_host = web_host[:-1]
    url = "{}://{}".format("https" if web_host_secure else "http", web_host)
    return url, web_host_secure, web_host


def _get_oauth_client_credentials():
    client_id = os.getenv('CLIENT_ID', '')
    if client_id == '':  # pragma: no cover
        raise NameError("Please add CLIENT_ID to your .env")
    client_secret = os.getenv('CLIENT_SECRET', '')
    if client_secret == '':  # pragma: no cover
        raise NameError("Please add CLIENT_SECRET to your .env")
    return client_id, client_secret


def run_service(run_forever=True, use_dotenv=True):
    """Kick off the service."""
    global SESSION
    global MOTOR_CONTROLLER
    global CHAINABLE_RGB_MANAGER
    global ROVERCODE_WEB_URL
    global ROVER_CONFIG
    global CLIENT_ID
    LOGGER.info("Starting the Rovercode service!")

    if use_dotenv:  # pragma: no cover
        load_dotenv('../.env')

    ROVERCODE_WEB_URL, web_host_secure, host = _get_web_url()
    CLIENT_ID, client_secret = _get_oauth_client_credentials()

    LOGGER.info("Targeting host %s. My client id is %s",
                ROVERCODE_WEB_URL, CLIENT_ID)

    if not web_host_secure:  # pragma: no cover
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    client = BackendApplicationClient(client_id=CLIENT_ID)
    global SESSION
    SESSION = OAuth2Session(client=client)
    SESSION.fetch_token(token_url='{}/oauth2/token/'.format(ROVERCODE_WEB_URL),
                        CLIENT_ID=CLIENT_ID,
                        client_secret=client_secret)

    # Get rover config info from server
    info = json.loads(SESSION.get('{}/api/v1/rovers?CLIENT_ID={}'.format(
        ROVERCODE_WEB_URL, CLIENT_ID)).text)['results'][0]
    LOGGER.info("Found myself - I am %s, with id %s",
                info[constants.ROVER_NAME], info[constants.ROVER_ID])
    ROVER_CONFIG = info[constants.ROVER_CONFIG]

    # Create chainable RGB LED manager
    chainable_rgb_led_count, chainable_rgb_led_port = \
        ROVER_CONFIG.get(constants.NUM_CHAINABLE_RGB_LEDS), \
        ROVER_CONFIG.get(constants.CHAINABLE_RGB_LED_PORT)
    if chainable_rgb_led_count is None:
        LOGGER.error(f'{constants.NUM_CHAINABLE_RGB_LEDS} missing from config')
        return
    if chainable_rgb_led_port is None:
        LOGGER.error(f'{constants.CHAINABLE_RGB_LED_PORT} missing from config')
        return
    CHAINABLE_RGB_MANAGER = ChainableRgbLedsManager(chainable_rgb_led_port,
                                                    chainable_rgb_led_count,
                                                    GrovePiChainableRgbLeds())

    # Create motor manager
    try:
        MOTOR_CONTROLLER = MotorController(
            GroveMotors(),
            ROVER_CONFIG.get(constants.MOTOR_REVERSE_LEFT_FIELD),
            ROVER_CONFIG.get(constants.MOTOR_REVERSE_RIGHT_FIELD))
    except:  # pylint: disable=bare-except
        CHAINABLE_RGB_MANAGER.set_all_led_colors(*constants.RGB_RED)

    # Create websocket connection
    try:
        ws_url = "{}://{}/ws/realtime/{}/".format(
            "wss" if web_host_secure else "ws", host, CLIENT_ID)
        auth_string = "Authorization: Bearer {}".format(SESSION.access_token)
        ws_connection = WebSocketApp(
            ws_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            header=[auth_string])
        ws_connection.on_open = on_open
        if run_forever:  # pragma: no cover
            ws_connection.run_forever()
    except:  # pylint: disable=bare-except
        CHAINABLE_RGB_MANAGER.set_all_led_colors(*constants.RGB_YELLOW)


if __name__ == '__main__':  # pragma: no cover
    run_service()

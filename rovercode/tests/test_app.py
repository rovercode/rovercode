"""Test the app module."""
import json
import os
from unittest.mock import MagicMock, patch
import functools
from multiprocessing import SimpleQueue
import pytest

import constants


@pytest.fixture()
def rover_params():
    """Rover parameters."""
    params = {
        constants.ROVER_NAME: 'rovy mcroverface',
        constants.ROVER_ID: 42,
        constants.ROVER_CONFIG: {
            constants.LEFT_ULTRASONIC_PORT: 1,
            constants.RIGHT_ULTRASONIC_PORT: 2,
            constants.LEFT_ULTRASONIC_THRESHOLD: 30,
            constants.RIGHT_ULTRASONIC_THRESHOLD: 40,
            constants.NUM_CHAINABLE_RGB_LEDS: 2,
            constants.CHAINABLE_RGB_LED_PORT: 3
        }
    }
    yield params


class TestQueue:
    """A simple one-item queue to use for testing."""

    def __init__(self):
        """Create an empty queue."""
        self.thing = None

    def put(self, thing):
        """Put an item on the queue."""
        self.thing = thing

    def get(self):
        """Pop the item from the queue."""
        thing = self.thing
        self.thing = None
        return thing

    def empty(self):
        """Return True if there is no item."""
        return self.thing is None


def test_app_send_heartbeat(testapp):
    """Test sending the heartbeat."""
    websocket = MagicMock()
    testapp.send_heartbeat(websocket, run_once_only=True)
    websocket.send.assert_called_with(
        json.dumps({constants.MESSAGE_TYPE: constants.HEARTBEAT_TYPE}))


def test_app_poll_sensors(testapp):
    """Test the function that polls the sensors."""
    sensor_message = {
        constants.MESSAGE_TYPE: constants.SENSOR_READING_TYPE,
        constants.SENSOR_TYPE_FIELD: constants.SENSOR_TYPE_BINARY,
        constants.UNIT_FIELD: constants.SENSOR_UNIT_ACTIVE_HIGH,
        constants.SENSOR_ID_FIELD: 'left-eye',
        constants.SENSOR_VALUE_FIELD: True
    }
    websocket = MagicMock()
    sensor = MagicMock()
    sensor.name = 'left-eye'
    sensor.get_change.return_value = True
    binary_sensors = [sensor]
    testapp.grovepi_thread_loop(websocket, binary_sensors, run_once_only=True)
    websocket.send.assert_called()
    assert sensor_message == json.loads(websocket.send.call_args[0][0])


def test_app_on_chainable_led_message(testapp):
    """Test an incoming chainable RGB LED message."""
    websocket = MagicMock()
    testapp.GROVEPI_QUEUE = SimpleQueue()
    testapp.CHAINABLE_RGB_MANAGER = MagicMock()
    # SimpleQueue has trouble pickling MagicMocks, so let's just use `print`
    testapp.CHAINABLE_RGB_MANAGER.set_led_color = print
    testapp.on_message(websocket, json.dumps({
        constants.MESSAGE_TYPE: constants.CHAINABLE_RGB_LED_COMMAND,
        constants.CHAINABLE_RGB_LED_ID_FIELD: 0,
        constants.CHAINABLE_RGB_LED_RED_VALUE_FIELD: 50,
        constants.CHAINABLE_RGB_LED_GREEN_VALUE_FIELD: 255,
        constants.CHAINABLE_RGB_LED_BLUE_VALUE_FIELD: 80
    }))
    expected = functools.partial(print, 0, 50, 255, 80)
    assert_partials_equal(expected, testapp.GROVEPI_QUEUE.get())


def test_app_grovepi_thread_action(testapp):
    """Test finding an action on the GrovePi thread loop."""
    websocket = MagicMock()
    action = MagicMock()
    # SimpleQueue can't pickle a MagicMock, so let's use the simpler TestQueue
    testapp.GROVEPI_QUEUE = TestQueue()
    testapp.GROVEPI_QUEUE.put(functools.partial(action, 'foobar_arg'))
    testapp.grovepi_thread_loop(websocket, [], run_once_only=True)
    action.assert_called_with("foobar_arg")
    assert testapp.GROVEPI_QUEUE.empty()


def test_app_grovepi_thread_action_error(testapp):
    """Test an action that errors on the GrovePi thread loop."""
    websocket = MagicMock()
    action = MagicMock()
    action.side_effect = ValueError("wrong value")
    # SimpleQueue can't pickle a MagicMock, so let's use the simpler TestQueue
    testapp.GROVEPI_QUEUE = TestQueue()
    testapp.GROVEPI_QUEUE.put(functools.partial(action, "foobar_arg"))
    testapp.grovepi_thread_loop(websocket, [], run_once_only=True)
    action.assert_called_with("foobar_arg")
    assert testapp.GROVEPI_QUEUE.empty()
    # Assert only that the exception is handled


def assert_partials_equal(expected, actual):
    """Assert that two wrapped partial functions are equal."""
    assert expected.func == actual.func
    assert expected.args == actual.args
    assert expected.keywords == actual.keywords


def test_app_on_motor_message(testapp):
    """Test an incoming motor message."""
    websocket = MagicMock()
    mock_motor_controller = MagicMock()
    testapp.MOTOR_CONTROLLER = mock_motor_controller
    testapp.on_message(websocket, json.dumps({
        constants.MESSAGE_TYPE: constants.MOTOR_COMMAND,
        constants.MOTOR_ID_FIELD: constants.LEFT_MOTOR,
        constants.MOTOR_VALUE_FIELD: 80,
        constants.MOTOR_DIRECTION_FIELD: constants.MOTOR_DIRECTION_FORWARD
    }))
    mock_motor_controller.set_speed.assert_called_with(
        constants.LEFT_MOTOR,
        80,
        constants.MOTOR_DIRECTION_FORWARD)


def test_app_on_message_invalid_motor(testapp):
    """Test an incoming motor message with an invalid motor."""
    websocket = MagicMock()
    mock_motor_controller = MagicMock()
    testapp.motor_controller = mock_motor_controller
    testapp.on_message(websocket, json.dumps({
        constants.MESSAGE_TYPE: constants.MOTOR_COMMAND,
        constants.MOTOR_ID_FIELD: 'not a motor',
        constants.MOTOR_VALUE_FIELD: 80
    }))
    mock_motor_controller.set_speed.assert_not_called()


def test_app_on_open_success(testapp, rover_params):
    """Test that the threads are started on websocket open."""
    websocket = MagicMock()
    testapp.ROVER_CONFIG = rover_params[constants.ROVER_CONFIG]
    testapp.CHAINABLE_RGB_MANAGER = MagicMock()

    heartbeat_function = MagicMock()
    grovepi_thread_loop = MagicMock()
    testapp.send_heartbeat = heartbeat_function
    testapp.grovepi_thread_loop = grovepi_thread_loop

    testapp.on_open(websocket)
    heartbeat_function.assert_called()
    grovepi_thread_loop.assert_called()


def test_app_main(testapp, rover_params):
    """Smoke test of the main function."""
    env_values = {'CLIENT_ID': 'foo',
                  'CLIENT_SECRET': 'bar',
                  'ROVERCODE_WEB_HOST': 'qux'}
    response = MagicMock()
    response.text = json.dumps({'results': [rover_params]})
    session = MagicMock()
    session.fetch_token.return_value = 'baz'
    session.get.return_value = response
    session_wrapper = MagicMock()
    session_wrapper.return_value = session
    with patch.dict(os.environ, env_values):
        with patch.object(testapp, 'OAuth2Session', session_wrapper):
            testapp.run_service(run_forever=False, use_dotenv=False)


def test_app_main_missing_led_count(testapp, rover_params):
    """Smoke test that the main function returns with no LED count."""
    env_values = {'CLIENT_ID': 'foo',
                  'CLIENT_SECRET': 'bar',
                  'ROVERCODE_WEB_HOST': 'qux'}
    rover_params[constants.ROVER_CONFIG].pop(constants.NUM_CHAINABLE_RGB_LEDS)
    response = MagicMock()
    response.text = json.dumps({'results': [rover_params]})
    session = MagicMock()
    session.fetch_token.return_value = 'baz'
    session.get.return_value = response
    session_wrapper = MagicMock()
    session_wrapper.return_value = session
    with patch.dict(os.environ, env_values):
        with patch.object(testapp, 'OAuth2Session', session_wrapper):
            testapp.run_service(run_forever=False, use_dotenv=False)


def test_app_main_missing_led_port(testapp, rover_params):
    """Smoke test that the main function returns with no LED port."""
    env_values = {'CLIENT_ID': 'foo',
                  'CLIENT_SECRET': 'bar',
                  'ROVERCODE_WEB_HOST': 'qux'}
    rover_params[constants.ROVER_CONFIG].pop(constants.CHAINABLE_RGB_LED_PORT)
    response = MagicMock()
    response.text = json.dumps({'results': [rover_params]})
    session = MagicMock()
    session.fetch_token.return_value = 'baz'
    session.get.return_value = response
    session_wrapper = MagicMock()
    session_wrapper.return_value = session
    with patch.dict(os.environ, env_values):
        with patch.object(testapp, 'OAuth2Session', session_wrapper):
            testapp.run_service(run_forever=False, use_dotenv=False)


def test_app_main_motor_exception(testapp, rover_params):
    """Smoke test that the main function returns with no LED port."""
    env_values = {'CLIENT_ID': 'foo',
                  'CLIENT_SECRET': 'bar',
                  'ROVERCODE_WEB_HOST': 'qux'}
    response = MagicMock()
    response.text = json.dumps({'results': [rover_params]})
    session = MagicMock()
    session.fetch_token.return_value = 'baz'
    session.get.return_value = response
    session_wrapper = MagicMock()
    session_wrapper.return_value = session
    bad_controller = MagicMock()
    bad_controller.side_effect = Exception('Motors broke')
    with patch.dict(os.environ, env_values):
        with patch.object(testapp, 'OAuth2Session', session_wrapper):
            with patch.object(testapp, 'MotorController', bad_controller):
                testapp.run_service(run_forever=False, use_dotenv=False)


def test_app_main_websocket_exception(testapp, rover_params):
    """Smoke test that the main function returns with no LED port."""
    env_values = {'CLIENT_ID': 'foo',
                  'CLIENT_SECRET': 'bar',
                  'ROVERCODE_WEB_HOST': 'qux'}
    response = MagicMock()
    response.text = json.dumps({'results': [rover_params]})
    session = MagicMock()
    session.fetch_token.return_value = 'baz'
    session.get.return_value = response
    session_wrapper = MagicMock()
    session_wrapper.return_value = session
    bad_websocket = MagicMock()
    bad_websocket.side_effect = Exception('LEDs broke')
    with patch.dict(os.environ, env_values):
        with patch.object(testapp, 'OAuth2Session', session_wrapper):
            with patch.object(testapp, 'WebSocketApp', bad_websocket):
                testapp.run_service(run_forever=False, use_dotenv=False)

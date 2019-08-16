"""Test the app module."""
import json
import os
from unittest.mock import MagicMock, patch
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
    testapp.poll_sensors(websocket, binary_sensors, run_once_only=True)
    websocket.send.assert_called()
    assert sensor_message == json.loads(websocket.send.call_args[0][0])


def test_app_on_chainable_led_message(testapp):
    """Test an incoming chainable RGB LED message."""
    websocket = MagicMock()
    mock_rgb_manager = MagicMock()
    mock_rgb_manager.count = 10
    testapp.CHAINABLE_RGB_MANAGER = mock_rgb_manager
    testapp.on_message(websocket, json.dumps({
        constants.MESSAGE_TYPE: constants.CHAINABLE_RGB_LED_COMMAND,
        constants.CHAINABLE_RGB_LED_ID_FIELD: 0,
        constants.CHAINABLE_RGB_LED_RED_VALUE_FIELD: 50,
        constants.CHAINABLE_RGB_LED_GREEN_VALUE_FIELD: 255,
        constants.CHAINABLE_RGB_LED_BLUE_VALUE_FIELD: 80
    }))
    mock_rgb_manager.set_led_color.assert_called_with(0, 50, 255, 80)


def test_app_on_chainable_led_message_error_setting_color(testapp):
    """Test an incoming chainable RGB LED message with a bad id."""
    websocket = MagicMock()
    mock_rgb_manager = MagicMock()
    mock_rgb_manager.set_led_color.side_effect = ValueError("wrong value")
    testapp.CHAINABLE_RGB_MANAGER = mock_rgb_manager
    testapp.on_message(websocket, json.dumps({
        constants.MESSAGE_TYPE: constants.CHAINABLE_RGB_LED_COMMAND,
        constants.CHAINABLE_RGB_LED_ID_FIELD: 1,
        constants.CHAINABLE_RGB_LED_RED_VALUE_FIELD: 50,
        constants.CHAINABLE_RGB_LED_GREEN_VALUE_FIELD: 255,
        constants.CHAINABLE_RGB_LED_BLUE_VALUE_FIELD: 80
    }))
    # Check only that exception is handled.


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
    polling_function = MagicMock()
    testapp.send_heartbeat = heartbeat_function
    testapp.poll_sensors = polling_function

    testapp.on_open(websocket)
    heartbeat_function.assert_called()
    polling_function.assert_called()


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

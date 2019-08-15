"""Test the app module."""
import json
import os
from unittest.mock import MagicMock, patch

import constants

ROVER_PARAMS = {
    constants.ROVER_NAME: 'rovy mcroverface',
    constants.ROVER_ID: 42,
    constants.ROVER_CONFIG: {
        constants.LEFT_ULTRASONIC_PORT: 1,
        constants.RIGHT_ULTRASONIC_PORT: 2,
        constants.LEFT_ULTRASONIC_THRESHOLD: 30,
        constants.RIGHT_ULTRASONIC_THRESHOLD: 40,
    }
}


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


def test_app_on_message(testapp):
    """Test the websocket incoming message handler."""
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
    """Test the websocket incoming message handler."""
    websocket = MagicMock()
    mock_motor_controller = MagicMock()
    testapp.motor_controller = mock_motor_controller
    testapp.on_message(websocket, json.dumps({
        constants.MESSAGE_TYPE: constants.MOTOR_COMMAND,
        constants.MOTOR_ID_FIELD: 'not a motor',
        constants.MOTOR_VALUE_FIELD: 80
    }))
    mock_motor_controller.set_speed.assert_not_called()


def test_app_on_open_success(testapp):
    """Test that the threads are started on websocket open."""
    websocket = MagicMock()
    testapp.ROVER_CONFIG = ROVER_PARAMS[constants.ROVER_CONFIG]
    testapp.CHAINABLE_RGB_MANAGER = MagicMock()

    heartbeat_function = MagicMock()
    polling_function = MagicMock()
    testapp.send_heartbeat = heartbeat_function
    testapp.poll_sensors = polling_function

    testapp.on_open(websocket)
    heartbeat_function.assert_called()
    polling_function.assert_called()


def test_app_main(testapp):
    """Smoke test of the main function."""
    env_values = {'CLIENT_ID': 'foo',
                  'CLIENT_SECRET': 'bar',
                  'ROVERCODE_WEB_HOST': 'qux'}
    response = MagicMock()
    response.text = json.dumps({'results': [ROVER_PARAMS]})
    session = MagicMock()
    session.fetch_token.return_value = 'baz'
    session.get.return_value = response
    session_wrapper = MagicMock()
    session_wrapper.return_value = session
    with patch.dict(os.environ, env_values):
        with patch.object(testapp, 'OAuth2Session', session_wrapper):
            testapp.run_service(run_forever=False, use_dotenv=False)

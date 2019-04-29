"""Test the app module."""
import json
import pytest
import os
from mock import MagicMock, patch

import constants

ROVER_PARAMS = {
    constants.ROVER_NAME: 'rovy mcroverface',
    constants.ROVER_ID: 42,
    constants.ROVER_CONFIG: {
        constants.LEFT_EYE_I2C_PORT: 1,
        constants.RIGHT_EYE_I2C_PORT: 2,
        constants.LEFT_EYE_I2C_ADDR: 3,
        constants.RIGHT_EYE_I2C_ADDR: 4,
        constants.LEFT_MOTOR_PORT: 'a',
        constants.RIGHT_MOTOR_PORT: 'b',
    }
}


def test_app_init_inputs(testapp):
    """Test the initialization of the sensors."""
    binary_sensors = testapp.init_inputs(ROVER_PARAMS[constants.ROVER_CONFIG])
    assert len(binary_sensors) == 2
    assert binary_sensors[0].sensor.i2c_addr == 3
    assert binary_sensors[1].sensor.i2c_addr == 4


def test_app_send_heartbeat(testapp):
    """Test sending the heartbeat."""
    ws = MagicMock()
    testapp.send_heartbeat(ws, run_once_only=True)
    ws.send.assert_called_with(
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
    ws = MagicMock()
    sensor = MagicMock()
    sensor.name = 'left-eye'
    sensor.get_change.return_value = True
    binary_sensors = [sensor]
    testapp.poll_sensors(ws, binary_sensors, run_once_only=True)
    ws.send.assert_called()
    assert sensor_message == json.loads(ws.send.call_args[0][0])


def test_app_init_dummy_inputs(testapp):
    """Test the initialization of the sensors in dummy mode."""
    binary_sensors = testapp.init_inputs(ROVER_PARAMS, dummy=True)
    assert len(binary_sensors) == 2


def test_app_on_message(testapp):
    """Test the websocket incoming message handler."""
    ws = MagicMock()
    mock_motor_controller = MagicMock()
    testapp.motor_controller = mock_motor_controller
    testapp.on_message(ws, json.dumps({
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
    ws = MagicMock()
    mock_motor_controller = MagicMock()
    testapp.motor_controller = mock_motor_controller
    testapp.on_message(ws, json.dumps({
        constants.MESSAGE_TYPE: constants.MOTOR_COMMAND,
        constants.MOTOR_ID_FIELD: 'not a motor',
        constants.MOTOR_VALUE_FIELD: 80
    }))
    mock_motor_controller.set_speed.assert_not_called()


def test_app_on_open(testapp):
    """Test that the threads are started on websocket open."""
    ws = MagicMock()
    response = MagicMock()
    response.text = json.dumps({'results': [ROVER_PARAMS]})
    mock_session = MagicMock()
    mock_session.get.return_value = response
    testapp.session = mock_session
    testapp.rovercode_web_url = 'foo'
    testapp.client_id = 'bar'

    heartbeat_function = MagicMock()
    polling_function = MagicMock()
    testapp.send_heartbeat = heartbeat_function
    testapp.poll_sensors = polling_function

    testapp.on_open(ws)
    heartbeat_function.assert_called()
    polling_function.assert_called()
    assert testapp.motor_controller is not None


def test_app_on_open_missing_config(testapp):
    """Test that the threads are started on websocket open."""
    ws = MagicMock()
    response = MagicMock()
    ROVER_PARAMS[constants.ROVER_CONFIG] = {}
    response.text = json.dumps({'results': [ROVER_PARAMS]})
    mock_session = MagicMock()
    mock_session.get.return_value = response
    testapp.session = mock_session
    testapp.rovercode_web_url = 'foo'
    testapp.client_id = 'bar'

    with pytest.raises(ValueError):
        testapp.on_open(ws)


def test_app_main(testapp):
    """Smoke test of the main function."""
    env_values = {'CLIENT_ID': 'foo',
                  'CLIENT_SECRET': 'bar',
                  'ROVERCODE_WEB_HOST': 'qux'}
    session = MagicMock()
    session.fetch_token.return_value = 'baz'
    with patch.dict(os.environ, env_values):
        with patch.object(testapp, 'OAuth2Session', session):
            testapp.run_service(run_forever=False, use_dotenv=False)

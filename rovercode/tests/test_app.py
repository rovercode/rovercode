"""Test the app module."""
import responses
import re
import json
from mock import MagicMock, patch

import constants

TEST_URL = "http://a.com/"

ROVER_PARAMS = {
    constants.ROVER_NAME: 'rovy mcroverface',
    constants.ROVER_ID: 42,
    constants.LEFT_EYE_I2C_PORT: 1,
    constants.RIGHT_EYE_I2C_PORT: 2,
    constants.LEFT_EYE_I2C_ADDR: 3,
    constants.RIGHT_EYE_I2C_ADDR: 4,
    constants.LEFT_FORWARD_PIN: 5,
    constants.LEFT_BACKWARD_PIN: 5,
    constants.RIGHT_FORWARD_PIN: 6,
    constants.RIGHT_BACKWARD_PIN: 7
}

def test_app_init_inputs(testapp):
    """Test the initialization of the sensors."""
    binary_sensors = testapp.init_inputs(ROVER_PARAMS)
    assert len(binary_sensors) == 2
    assert binary_sensors[0].sensor.i2c_addr == 3
    assert binary_sensors[1].sensor.i2c_addr == 4


def test_app_send_heartbeat(testapp):
    """Test sending the heartbeat."""
    ws = MagicMock()
    testapp.send_heartbeat(ws, run_once_only=True)
    ws.send.assert_called_with(json.dumps({constants.MESSAGE_TYPE: constants.HEARTBEAT_TYPE}))


def test_app_poll_sensors(testapp):
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
        constants.MOTOR_VALUE_FIELD: 80
    }))
    mock_motor_controller.set_speed.assert_called_with(constants.LEFT_MOTOR, 80)


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
    response.text = json.dumps([ROVER_PARAMS])
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


def test_app_main(testapp):
    """Smoke test of the main function."""
    testapp.run_service(run_forever=False)



# @responses.activate
# def test_register_with_web_create(testapp):
#     """Test the rover registering with rovercode-web."""
#     testapp.set_rovercodeweb_url(TEST_URL)
#     testapp.rover_name = "curiosity"
#     payload = {'name': 'Chipy',
#                'local_ip': '2.2.2.2'}
#     web_id = 333
#     access_token = '1234'
#     testapp.binary_sensors = []
#     response_payload = payload.copy()
#     response_payload['id'] = web_id
#
#     responses.add(responses.POST, testapp.ROVERCODE_WEB_OAUTH2_URL + '/',
#                   json={'access_token': access_token}, status=200,
#                   content_type='application/json',
#     )
#     responses.add(responses.POST, testapp.ROVERCODE_WEB_OAUTH2_URL + '/',
#                   json='', status=200,
#                   content_type='application/json',
#     )
#     responses.add(responses.POST, testapp.ROVERCODE_WEB_REG_URL + '/',
#                   json=response_payload, status=200,
#                   content_type='application/json'
#     )
#
#     #test init()
#     heartbeat_manager = testapp.HeartBeatManager(client_id='xxxx',
#                                                  client_secret="asdf")
#     assert access_token in heartbeat_manager.auth_header['Authorization']
#     assert len(responses.calls) == 1
#     assert responses.calls[0].request.url == testapp.ROVERCODE_WEB_OAUTH2_URL + '/'
#
#
# @responses.activate
# def test_register_with_web_update(testapp):
#     """Test the periodic hearbeat for a rover that is already registered."""
#     testapp.set_rovercodeweb_url(TEST_URL)
#     testapp.rover_name = "curiosity"
#     testapp.binary_sensors = []
#     web_id = '444'
#     payload = {'name': testapp.rover_name,
#                'web_id': web_id,
#                'left_eye_i2c_port': 5,
#                'left_eye_i2c_addr': 6,
#                'right_eye_i2c_port': 7,
#                'right_eye_i2c_addr': 8,
#                'local_ip': '2.2.2.2'}
#     access_token = '1234'
#     response_payload = payload.copy()
#     response_payload['id'] = web_id
#
#     responses.add(responses.POST, testapp.ROVERCODE_WEB_OAUTH2_URL + '/',
#                   json={'access_token': access_token}, status=200,
#                   content_type='application/json',
#     )
#     responses.add(responses.POST, testapp.ROVERCODE_WEB_REG_URL + '/',
#                   json=response_payload, status=200,
#                   content_type='application/json'
#     )
#     url_re = re.compile(testapp.ROVERCODE_WEB_REG_URL + r'\?client_id=xxxx')
#     response_list = [response_payload]
#     responses.add(responses.GET,
#                   url_re,
#                   json=response_list, status=200,
#                   content_type='application/json'
#     )
#     responses.add(responses.PUT, testapp.ROVERCODE_WEB_REG_URL+'/'+str(web_id)+'/',
#                   json=response_payload, status=200,
#                   content_type='application/json'
#     )
#
#     heartbeat_manager = testapp.HeartBeatManager(client_id='xxxx',
#                                                  client_secret="asdf")
#     heartbeat_manager.thread_func(run_once=True)
#     # test the side-effects of read()
#     assert heartbeat_manager.web_id == web_id
#     assert len(testapp.binary_sensors) == 2
#     assert testapp.binary_sensors[0].sensor.i2c_addr == 6
#     assert testapp.binary_sensors[1].sensor.i2c_addr == 8
#     assert len(responses.calls) == 3
#     assert responses.calls[0].request.url == testapp.ROVERCODE_WEB_OAUTH2_URL + '/'
#     assert responses.calls[1].request.url == testapp.ROVERCODE_WEB_REG_URL + '?client_id=xxxx'
#     # test that the update happened
#     assert responses.calls[2].request.url == testapp.ROVERCODE_WEB_REG_URL + '/' + str(web_id) + '/'

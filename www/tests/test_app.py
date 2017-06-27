"""Test the app module."""
import responses
import re

TEST_URL = "http://a.com/"

def test_sensor_init(testapp):
    """Test the initialization of the sensors."""
    testapp.init_rover_service()
    assert len(testapp.binary_sensors) > 0

def test_get_local_ip(testapp):
    """Test that the rover can get its local ip address."""
    # quick and dirty test that it gets something of the form X.X.X.X
    assert len(testapp.get_local_ip().split('.')) == 4

@responses.activate
def test_register_with_web_create(testapp):
    """Test the rover registering with rovercode-web."""
    testapp.set_rovercodeweb_url(TEST_URL)
    testapp.rover_name = "curiosity"
    payload = {'name': 'Chipy', 'local_ip': '2.2.2.2'}
    web_id = 333
    response_payload = payload.copy()
    response_payload['id'] = web_id

    responses.add(responses.GET, testapp.ROVERCODE_WEB_LOGIN_URL + '/',
                  json='', status=200,
                  content_type='application/json',
    )
    responses.add(responses.POST, testapp.ROVERCODE_WEB_LOGIN_URL + '/',
                  json='', status=200,
                  content_type='application/json',
    )
    responses.add(responses.POST, testapp.ROVERCODE_WEB_REG_URL + '/',
                  json=response_payload, status=200,
                  content_type='application/json'
    )
    heartbeat_manager = testapp.HeartBeatManager(payload=payload,
                                                 user_name='Bob',
                                                 user_pass="asdf")
    result = heartbeat_manager.create()
    assert result.status_code == 200
    assert heartbeat_manager.web_id == web_id
    assert len(responses.calls) == 3
    assert responses.calls[0].request.url == testapp.ROVERCODE_WEB_LOGIN_URL + '/'
    assert responses.calls[1].request.url == testapp.ROVERCODE_WEB_LOGIN_URL + '/'
    assert responses.calls[2].request.url == testapp.ROVERCODE_WEB_REG_URL + '/'

@responses.activate
def test_register_with_web_update(testapp):
    """Test the periodic hearbeat for a rover that is already registered."""
    testapp.set_rovercodeweb_url(TEST_URL)
    testapp.rover_name = "curiosity"
    payload = {'name': testapp.rover_name, 'local_ip': '2.2.2.2'}
    web_id = 444
    response_payload = payload.copy()
    response_payload['id'] = web_id

    responses.add(responses.GET, testapp.ROVERCODE_WEB_LOGIN_URL + '/',
                  json='', status=200,
                  content_type='application/json',
    )
    responses.add(responses.POST, testapp.ROVERCODE_WEB_LOGIN_URL + '/',
                  json='', status=200,
                  content_type='application/json',
    )
    responses.add(responses.POST, testapp.ROVERCODE_WEB_REG_URL + '/',
                  json=response_payload, status=200,
                  content_type='application/json'
    )
    url_re = re.compile(testapp.ROVERCODE_WEB_REG_URL + r'\?name=' + testapp.rover_name)
    response_list = [response_payload]
    responses.add(responses.GET,
                  url_re,
                  json=response_list, status=200,
                  content_type='application/json'
    )
    responses.add(responses.PUT, testapp.ROVERCODE_WEB_REG_URL+'/'+str(web_id)+'/',
                  json=response_payload, status=200,
                  content_type='application/json'
    )

    heartbeat_manager = testapp.HeartBeatManager(id=web_id,
                                                 payload=payload,
                                                 user_name='Bob',
                                                 user_pass="asdf")
    heartbeat_manager.create()
    result = heartbeat_manager.thread_func(run_once=True)
    assert result.status_code == 200
    assert len(responses.calls) == 5
    assert responses.calls[0].request.url == testapp.ROVERCODE_WEB_LOGIN_URL + '/'
    assert responses.calls[1].request.url == testapp.ROVERCODE_WEB_LOGIN_URL + '/'
    assert responses.calls[2].request.url == testapp.ROVERCODE_WEB_REG_URL + '/'
    assert responses.calls[3].request.url == testapp.ROVERCODE_WEB_REG_URL + '?name=' + testapp.rover_name
    assert responses.calls[4].request.url == testapp.ROVERCODE_WEB_REG_URL + '/' + str(web_id)+'/'

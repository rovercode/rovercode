"""Test the app module."""
import app
import responses

def test_sensor_init():
    """Test the initialization of the sensors."""
    assert len(app.binary_sensors) > 0

def test_get_local_ip():
    """Test that the rover can get its local ip address."""
    # quick and dirty test that it gets something of the form X.X.X.X
    assert len(app.get_local_ip().split('.')) == 4

@responses.activate
def test_register_with_web():
    """Test the rover registering with rovercode-web."""
    payload = {'name': 'Chipy', 'owner': 'Mr. Hurlburt', 'local_ip': '2.2.2.2'}
    web_id = 333
    heartbeat_manager = app.HeartBeatManager(payload=payload)
    response_payload = payload.copy()
    response_payload['id'] = web_id
    responses.add(responses.POST, app.ROVERCODE_WEB_REG_URL,
                  json=response_payload, status=200,
                  content_type='application/json')
    result = heartbeat_manager.register()
    assert result.status_code == 200
    assert heartbeat_manager.web_id == web_id
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == app.ROVERCODE_WEB_REG_URL

@responses.activate
def test_heartbeat_thread():
    """Test the periodic hearbeat for a rover that is already registered."""
    payload = {'name': 'Chipy2', 'owner': 'Mr. Hurlburt', 'local_ip': '2.2.2.2'}
    web_id = 444
    response_payload = payload.copy()
    response_payload['id'] = web_id
    heartbeat_manager = app.HeartBeatManager(id=web_id, payload=payload)

    responses.add(responses.PUT, app.ROVERCODE_WEB_REG_URL+str(web_id)+"/",
                  json=response_payload, status=200,
                  content_type='application/json')

    result = heartbeat_manager.thread_func(run_once=True)
    assert result.status_code == 200
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == app.ROVERCODE_WEB_REG_URL+str(web_id)+"/"

@responses.activate
def test_heartbeat_thread_forgotten():
    """Test the periodic heartbeat for a rover forgotten by the server."""
    web_id = 555
    payload = {'name': 'Chipy3', 'owner': 'Mr. Hurlburt', 'local_ip': '2.2.2.2'}
    response_payload = payload.copy()
    response_payload['id'] = web_id
    heartbeat_manager = app.HeartBeatManager(id=web_id, payload=payload)

    responses.add(responses.PUT, app.ROVERCODE_WEB_REG_URL+str(web_id)+"/",
                  json=None, status=404,
                  content_type='application/json')

    responses.add(responses.POST, app.ROVERCODE_WEB_REG_URL,
                  json=response_payload, status=200,
                  content_type='application/json')

    result = heartbeat_manager.thread_func(run_once=True)
    assert result.status_code == 200
    assert heartbeat_manager.web_id == web_id

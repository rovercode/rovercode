import app
import responses
import requests

def test_sensor_init():
    assert len(app.binary_sensors) > 0

def test_get_local_ip():
    # quick and dirty test that it gets something of the form X.X.X.X
    assert len(app.get_local_ip().split('.')) == 4

@responses.activate
def test_register_with_web():
    payload = {'name': 'Chipy', 'owner': 'Mr. Hurlburt', 'local_ip': '2.2.2.2'}
    heartbeat_manager = app.HeartBeatManager(payload=payload)
    response_payload = payload.copy()
    response_payload['id'] = 333
    responses.add(responses.POST, app.ROVERCODE_WEB_REG_URL,
                  json=response_payload, status=200,
                  content_type='application/json')

    assert app.heartbeat_manager.register().status_code in [200, 201]

@responses.activate
def test_heartbeat_thread():
    payload = {'name': 'Chipy2', 'owner': 'Mr. Hurlburt', 'local_ip': '2.2.2.2'}
    web_id = 444
    response_payload = payload.copy()
    response_payload['id'] = 333
    heartbeat_manager = app.HeartBeatManager(id=web_id, payload=payload)

    responses.add(responses.PUT, app.ROVERCODE_WEB_REG_URL+str(web_id)+"/",
                  json=response_payload, status=200,
                  content_type='application/json')

    result = heartbeat_manager.thread_func(run_once=True)
    assert result.status_code in [200, 201]

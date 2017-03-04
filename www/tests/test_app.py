import app
import responses
import requests
import json

def test_sensor_init():
    assert len(app.binary_sensors) > 0

def test_get_local_ip():
    # quick and dirty test that it gets something of the form X.X.X.X
    assert len(app.get_local_ip().split('.')) == 4

@responses.activate
def test_register_with_web():
    payload = {'name': 'Chipy', 'owner': 'Mr. Hurlburt', 'local_ip': '2.2.2.2'}
    web_id = 333
    heartbeat_manager = app.HeartBeatManager(payload=payload)
    response_payload = payload.copy()
    response_payload['id'] = 333
    responses.add(responses.POST, app.ROVERCODE_WEB_REG_URL,
                  json=response_payload, status=200,
                  content_type='application/json')
    result = heartbeat_manager.register()
    assert result.status_code in [200, 201]
    assert heartbeat_manager.web_id == web_id
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == app.ROVERCODE_WEB_REG_URL

@responses.activate
def test_heartbeat_thread():
    # Test for a rover that has already been registered
    payload = {'name': 'Chipy2', 'owner': 'Mr. Hurlburt', 'local_ip': '2.2.2.2'}
    web_id = 444
    response_payload = payload.copy()
    response_payload['id'] = web_id
    heartbeat_manager = app.HeartBeatManager(id=web_id, payload=payload)

    responses.add(responses.PUT, app.ROVERCODE_WEB_REG_URL+str(web_id)+"/",
                  json=response_payload, status=200,
                  content_type='application/json')

    result = heartbeat_manager.thread_func(run_once=True)
    assert result.status_code in [200, 201]
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == app.ROVERCODE_WEB_REG_URL+str(web_id)+"/"

    # Test for a rover who has been forgotten by the server
    web_id_new = 555
    response_payload_new = response_payload.copy()
    response_payload_new['id'] = web_id_new
    reregister_attempted = False

    responses.add(responses.PUT, app.ROVERCODE_WEB_REG_URL+str(web_id_new)+"/",
                  json=None, status=404,
                  content_type='application/json')

    responses.add(responses.POST, app.ROVERCODE_WEB_REG_URL,
                  json=response_payload_new, status=200,
                  content_type='application/json')

    heartbeat_manager.web_id = web_id_new
    result = heartbeat_manager.thread_func(run_once=True)
    assert result.status_code in [200, 201]
    assert heartbeat_manager.web_id == web_id_new

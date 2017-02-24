import app

def test_sensor_init():
    assert len(app.binary_sensors) > 0

def test_get_local_ip():
    # quick and dirty test that it gets something of the form X.X.X.X
    assert len(app.get_local_ip().split('.')) == 4

def test_register_with_web():
    assert app.register_with_web().status_code in [200, 201]

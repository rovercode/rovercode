"""Test the binary sensor abstraction."""
from mock import MagicMock

from binary_sensor import BinarySensor


def test_binary_sensor_change():
    sensor = MagicMock()
    binary_sensor = BinarySensor('test-sensor', sensor)

    sensor.is_high.return_value = True
    assert binary_sensor.get_change()

    sensor.is_high.return_value = False
    assert not binary_sensor.get_change()


def test_binary_sensor_no_change():
    sensor = MagicMock()
    binary_sensor = BinarySensor('test-sensor', sensor)

    sensor.is_high.return_value = False
    assert binary_sensor.get_change() is None

    sensor.is_high.return_value = True
    binary_sensor.get_change()
    assert binary_sensor.get_change() == None


def test_binary_sensor_error():
    sensor = MagicMock()
    binary_sensor = BinarySensor('test-sensor', sensor)

    sensor.is_high.side_effect = IOError("Can't reach sensor. I'm so sorry.")
    assert binary_sensor.get_change() is None

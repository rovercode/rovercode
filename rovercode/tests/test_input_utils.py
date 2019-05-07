"""Test the binary sensor abstraction."""
import pytest

import constants
from input_utils import init_inputs, DEFAULT_THRESHOLD

CONFIG = {
    constants.LEFT_ULTRASONIC_PORT: 1,
    constants.RIGHT_ULTRASONIC_PORT: 2,
    constants.LEFT_ULTRASONIC_THRESHOLD: 30,
    constants.RIGHT_ULTRASONIC_THRESHOLD: 40,
}


def test_app_init_inputs():
    """Test the initialization of the sensors."""
    binary_sensors = init_inputs(CONFIG)
    assert len(binary_sensors) == 2
    assert binary_sensors[0].sensor.port == 1
    assert binary_sensors[0].sensor.binary_threshold == 30
    assert binary_sensors[1].sensor.port == 2
    assert binary_sensors[1].sensor.binary_threshold == 40


def test_app_init_inputs_threshold_defaults():
    """Test the initialization of the sensors using default thresholds."""
    minimal_config = CONFIG.copy()
    minimal_config.pop(constants.RIGHT_ULTRASONIC_THRESHOLD)
    minimal_config.pop(constants.LEFT_ULTRASONIC_THRESHOLD)
    binary_sensors = init_inputs(minimal_config)
    assert len(binary_sensors) == 2
    assert binary_sensors[0].sensor.binary_threshold == DEFAULT_THRESHOLD
    assert binary_sensors[1].sensor.binary_threshold == DEFAULT_THRESHOLD


def test_app_init_bad_ports():
    """Test init fallback due to bad ports."""
    bad_config = CONFIG.copy()
    bad_config[constants.RIGHT_ULTRASONIC_PORT] = "not an int"
    with pytest.raises(ValueError):
        init_inputs(bad_config)


def test_app_init_bad_thresholds():
    """Test init fail due to bad thresholds."""
    bad_config = CONFIG.copy()
    bad_config[constants.RIGHT_ULTRASONIC_THRESHOLD] = "not an int"
    binary_sensors = init_inputs(bad_config)
    assert len(binary_sensors) == 2
    assert binary_sensors[0].sensor.binary_threshold == DEFAULT_THRESHOLD
    assert binary_sensors[1].sensor.binary_threshold == DEFAULT_THRESHOLD


def test_app_init_inputs_missing_ports():
    """Test failed sensor init when the ultrasonic ports are missing."""
    with pytest.raises(ValueError):
        init_inputs({})

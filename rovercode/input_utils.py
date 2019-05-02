"""Helper functions for managing inputs."""

import logging

import constants

from binary_sensor import BinarySensor
from drivers.grovepi_ultrasonic_ranger_binary \
    import GrovePiUltrasonicRangerBinary

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))


def init_inputs(rover_params):
    """Initialize input GPIO."""
    binary_sensors = []

    left_port, right_port = \
        rover_params.get(constants.LEFT_ULTRASONIC_PORT),\
        rover_params.get(constants.RIGHT_ULTRASONIC_PORT)
    if any((left_port is None, right_port is None)):
        raise ValueError('Required sensor port configuration'
                         'not present in Rover config')
    try:
        left_port = int(left_port)
        right_port = int(right_port)
    except ValueError as error:
        LOGGER.error("Unusable values %s and %s for ultrasonic ports",
                     left_port, right_port)
        raise error  # TODO: Set RGB LED to red

    left_threshold, right_threshold = \
        rover_params.get(constants.LEFT_ULTRASONIC_THRESHOLD), \
        rover_params.get(constants.RIGHT_ULTRASONIC_THRESHOLD)
    if any((left_threshold is None, right_threshold is None)):
        LOGGER.info("No ultrasonic sensor thresholds found in"
                    "Rover config. Using defaults.")
        left_threshold, right_threshold = 10, 10
    else:
        try:
            left_threshold = int(left_threshold)
            right_threshold = int(right_threshold)
        except ValueError:
            LOGGER.error("Unusable values %s and %s "
                         "for ultrasonic thresholds. Using defaults.",
                         left_threshold, right_threshold)
            left_threshold, right_threshold = 10, 10

    binary_sensors.append(
        BinarySensor(
            "left_ultra_sensor",
            GrovePiUltrasonicRangerBinary(left_port, left_threshold)))
    binary_sensors.append(
        BinarySensor(
            "right_ultra_sensor",
            GrovePiUltrasonicRangerBinary(right_port, right_threshold)))

    return binary_sensors

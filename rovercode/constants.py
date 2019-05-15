"""Constants."""

# Websocket protocol constants
MESSAGE_TYPE = 'type'
UNIT_FIELD = 'unit'

HEARTBEAT_TYPE = 'heartbeat'

MOTOR_COMMAND = 'motor-command'
MOTOR_ID_FIELD = 'motor-id'
MOTOR_VALUE_FIELD = 'motor-value'
MOTOR_DIRECTION_FIELD = 'direction'
MOTOR_DIRECTION_FORWARD = 'forward'
MOTOR_DIRECTION_BACKWARD = 'backward'
LEFT_MOTOR = 'left-motor'
RIGHT_MOTOR = 'right-motor'
MOTOR_IDS = (LEFT_MOTOR, RIGHT_MOTOR)

SENSOR_READING_TYPE = 'sensor-reading'
SENSOR_ID_FIELD = 'sensor-id'
SENSOR_TYPE_FIELD = 'sensor-type'
SENSOR_TYPE_BINARY = 'binary'
SENSOR_UNIT_ACTIVE_HIGH = 'active-high'
SENSOR_VALUE_FIELD = 'sensor-value'
SENSOR_NAME_LEFT = 'ultrasonic-left'
SENSOR_NAME_RIGHT = 'ultrasonic-right'

# Config constants
LEFT_MOTOR_PORT = 'left-motor-port'
RIGHT_MOTOR_PORT = 'right-motor-port'
LEFT_ULTRASONIC_PORT = 'left-ultrasonic-port'
LEFT_ULTRASONIC_THRESHOLD = 'left-ultrasonic-threshold'
RIGHT_ULTRASONIC_PORT = 'right-ultrasonic-port'
RIGHT_ULTRASONIC_THRESHOLD = 'right-ultrasonic-threshold'

# API constants
ROVER_NAME = 'name'
ROVER_ID = 'id'
ROVER_CONFIG = 'config'

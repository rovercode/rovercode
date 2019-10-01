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
LEFT_MOTOR = 'motor-left'
RIGHT_MOTOR = 'motor-right'
MOTOR_IDS = (LEFT_MOTOR, RIGHT_MOTOR)

CHAINABLE_RGB_LED_COMMAND = 'chainable-rgb-led-command'
CHAINABLE_RGB_LED_ID_FIELD = 'led-id'
CHAINABLE_RGB_LED_RED_VALUE_FIELD = 'red-value'
CHAINABLE_RGB_LED_GREEN_VALUE_FIELD = 'green-value'
CHAINABLE_RGB_LED_BLUE_VALUE_FIELD = 'blue-value'

SENSOR_READING_TYPE = 'sensor-reading'
SENSOR_ID_FIELD = 'sensor-id'
SENSOR_TYPE_FIELD = 'sensor-type'
SENSOR_TYPE_BINARY = 'binary'
SENSOR_UNIT_ACTIVE_HIGH = 'active-high'
SENSOR_VALUE_FIELD = 'sensor-value'
SENSOR_NAME_LEFT = 'ultrasonic-left'
SENSOR_NAME_RIGHT = 'ultrasonic-right'

# Config constants
LEFT_ULTRASONIC_PORT = 'left-ultrasonic-port'
LEFT_ULTRASONIC_THRESHOLD = 'left-ultrasonic-threshold'
RIGHT_ULTRASONIC_PORT = 'right-ultrasonic-port'
RIGHT_ULTRASONIC_THRESHOLD = 'right-ultrasonic-threshold'
CHAINABLE_RGB_LED_PORT = 'chainable-rgb-led-port'
NUM_CHAINABLE_RGB_LEDS = 'num-chainable-rgb-leds'

# API constants
ROVER_NAME = 'name'
ROVER_ID = 'id'
ROVER_CONFIG = 'config'

# RGB colors
RGB_BLUE = (0, 74, 255)
RGB_RED = (255, 0, 0)
RGB_YELLOW = (255, 255, 0)

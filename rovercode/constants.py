"""Constants."""

# Websocket protocol constants
MESSAGE_TYPE = 'type'
UNIT_FIELD = 'unit'

HEARTBEAT_TYPE = 'heartbeat'

MOTOR_COMMAND = 'motor-command'
MOTOR_ID_FIELD = 'motor-id'
MOTOR_VALUE_FIELD = 'motor-value'
LEFT_MOTOR = 'left-motor'
RIGHT_MOTOR = 'right-motor'
MOTOR_IDS = (LEFT_MOTOR, RIGHT_MOTOR)

SENSOR_READING_TYPE = 'sensor-reading'
SENSOR_ID_FIELD = 'sensor-id'
SENSOR_TYPE_FIELD = 'sensor-type'
SENSOR_TYPE_BINARY = 'binary'
SENSOR_UNIT_ACTIVE_HIGH = 'active-high'
SENSOR_VALUE_FIELD = 'sensor-value'

# API constants
ROVER_NAME = 'name'
ROVER_ID = 'id'
LEFT_EYE_I2C_PORT = 'left_eye_i2c_port'
LEFT_EYE_I2C_ADDR = 'left_eye_i2c_addr'
RIGHT_EYE_I2C_PORT = 'right_eye_i2c_port'
RIGHT_EYE_I2C_ADDR = 'right_eye_i2c_addr'
LEFT_FORWARD_PIN = 'left_forward_pin'
LEFT_BACKWARD_PIN = 'left_backward_pin'
RIGHT_FORWARD_PIN = 'right_forward_pin'
RIGHT_BACKWARD_PIN = 'right_backward_pin'

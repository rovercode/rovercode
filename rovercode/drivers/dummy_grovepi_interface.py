"""Dummy class to use when not running with real GrovePi hardware."""


class MiniMotorDriver:  # noqa
    """A dummy motor interface class."""

    def __init__(self, *args, **kwargs):  # noqa
        """Initialize the dummy driver."""
        return

    def stopMotors(self, *args, **kwargs):  # noqa
        """Stop the dummy motors."""
        return

    def stopLeftMotor(self, *args, **kwargs):  # noqa
        """Stop the left dummy motor."""
        return

    def stopRightMotor(self, *args, **kwargs):  # noqa
        """Stop the right dummy motor."""
        return

    def setLeftMotor(self, *args, **kwargs):  # noqa
        """Stop the left dummy motor."""
        return

    def setRightMotor(self, *args, **kwargs):  # noqa
        """Stop the right dummy motor."""
        return


def ultrasonicRead(port):  # noqa
    """Read from the dummy ultrasonic sensor."""
    return 0


def chainableRgbLed_pattern(pin, type, led):  # noqa
    pass


def storeColor(r, g, b):  # noqa
    pass


def chainableRgbLed_init(port, count):  # noqa
    pass


def pinMode(port, mode):  # noqa
    pass

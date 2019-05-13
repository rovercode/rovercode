"""Dummy class to use when not running with real GrovePi hardware."""


class motor_driver:  # noqa
    """A dummy motor interface class."""

    def MotorSpeedSetAB(self, *args, **kwargs):  # noqa
        """Set the dummy motor speed."""
        return

    def DirectionSet(self, *args, **kwargs):  # noqa
        """Set the dummy motor direction."""
        return


def ultrasonicRead(port):  # noqa
    """Read from the dummy ultrasonic sensor."""
    pass


def chainableRgbLed_pattern(pin, type, led):  # noqa
    pass


def storeColor(r, g, b):  # noqa
    pass


def chainableRgbLed_init(port, count):  # noqa
    pass


def pinMode(port, mode):  # noqa
    pass

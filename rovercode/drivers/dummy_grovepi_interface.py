"""Dummy class to use when not running with real GrovePi hardware."""


class motor_driver:  # nopep8
    """Dummy interface class."""

    def MotorSpeedSetAB(self, *args, **kwargs):  # nopep8
        """Dummy motor speed setter."""
        return

    def DirectionSet(self, *args, **kwargs):  # nopep8
        """Dummy motor direction setter."""
        return

"""A class to represent binary sensors."""

class BinarySensor:
    """
    The binary sensor object contains information for each binary sensor.

    :param name:
        The human readable name of the sensor
    :param sensor:
        The object representing the hardware sensor
    """

    def __init__(self, name, sensor):
        """Constructor for BinarySensor object."""
        self.name = name
        self.sensor = sensor
        self.old_val = False

    def get_change(self):
        try:
            new_val = self.sensor.is_high()
        except IOError:
            # Skip it and try again later
            return None
        if not self.old_val and new_val:
            ret = True
        elif self.old_val and not new_val:
            ret = False
        else:
            ret = None
        self.old_val = new_val
        return ret



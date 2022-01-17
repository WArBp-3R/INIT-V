from Device import Device


class Connection:
    """A connection between two devices represented by Device objects."""

    def __init__(self, first_device: Device, second_device: Device):
        """The constructor of the class."""
        self.first_device = first_device
        """The first device part of the connection."""
        self.second_device = second_device
        """The second device part of the connection."""
        # generate protocols list
        self.protocols

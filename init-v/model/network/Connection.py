from model.network.Device import Device


class Connection:
    """A connection between two devices represented by Device objects."""

    def __init__(self, first_device: Device, second_device: Device, protocols: set[str],
                 connection_information: dict[str, str],
                 protocol_connection_information: dict[str, dict[str, str]]):
        """The constructor of the class."""
        self.first_device = first_device
        """The first device part of the connection."""
        self.second_device = second_device
        """The second device part of the connection."""
        self.protocols = protocols
        """The protocols used on this connection."""
        self.connection_information: dict[str, str] = connection_information
        """Textual information of the connection as a whole"""
        self.protocol_connection_information: dict[str, dict[str, str]] = protocol_connection_information
        """Textual information of each protocol communication"""

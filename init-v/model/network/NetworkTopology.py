from model.network.Connection import Connection
from model.network.Device import Device


class NetworkTopology:
    """A network topology which consists of devices and connections between devices.
    A connection between two devices exist if at least one packet was sent from a device to the other device."""

    def __init__(self, devices: list[Device], connections: list[Connection], protocols: set[str], highest_protocols: set[str]):
        """The constructor of the class."""
        self.devices = devices
        """The devices in the topology."""
        self.connections = connections
        """The connections in the topology."""
        self.protocols = protocols
        self.highest_protocols = highest_protocols

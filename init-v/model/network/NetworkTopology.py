

class NetworkTopology:
    """A network topology which consists of devices and connections between devices.
    A connection between two devices exist if at least one packet was sent from a device to the other device."""

    def __init__(self, devices: list, connections: list):
        """The constructor of the class."""
        self.devices = devices
        """The devices in the topology."""
        self.connections = connections
        """The connections in the topology."""

    def update(self, active_protocols: list):
        """Updates the view of the network topology according to the selected protocols."""

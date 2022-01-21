
class Device:
    """A network device. The class contains attributes to uniquely identify the device."""

    def __init__(self, mac_address: str, ip_address: list[str]):
        """The constructor of the class."""
        self.mac_address = mac_address
        """The MAC address of the device."""
        self.ip_address = ip_address
        """The IP address of the device."""

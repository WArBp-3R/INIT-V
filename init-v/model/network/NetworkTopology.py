

class NetworkTopology:

    def __init__(self, devices: list, connections: list):
        self.devices = devices
        self.connections = connections

    def update(self, active_protocols: list):
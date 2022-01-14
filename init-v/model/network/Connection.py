
class Connection:

    def __init__(self, first_device: Device, second_device: Device):
        self.first_device = first_device
        self.second_device = second_device
        # generate protocols list
        self.protocols
from controller.init_v_controll_logic.BackendInterface import BackendInterface


class BackendAdapter (BackendInterface):

    def __init__(self, PCAP_ID: str):
        self.PCAP_ID = PCAP_ID

    def calculate_pca(self, PCAP_path: str, config: Configuration):
        #TODO implement PCAP_path???
        pass

    def calculate_autoencoder(self, PCAP_path: str, config: Configuration):
        #TODO implement
        pass

    def calculate_topology(self, PCAP_path: str, config: Configuration):
        #TODO
        pass
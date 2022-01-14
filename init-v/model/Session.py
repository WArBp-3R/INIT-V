from ModelInterface import ModelInterface
from network.NetworkTopology import NetworkTopology
from Configuration import Configuration
from RunResult import RunResult


class Session(ModelInterface):

    def __init__(self, PCAP_PATH: str, protocols: dict, run_results: list, active_config: Configuration,
                 topology: NetworkTopology):
        self.PCAP_PATH = PCAP_PATH
        self.protocols = protocols
        self.run_results = run_results
        self.active_config = active_config
        self.topology = topology

    def push_performance(self, pca: list, autoencoder: History):
        pass

    def push_methods(self, pca_result: list):
        pass

    def push_topology(self, topology: NetworkTopology):
        pass

    def push_statistics(self, stats: list):
        pass

    def push_configuration(self, config: Configuration):
        pass

    def compare_performance(self, pca: list, autoencoder: History, pos: list):
        pass

    def compare_methods(self, pca_result: list, autoencoder: list, pos: list):
        pass

    def compare_statistics(self, stats: list, pos: list):
        pass

    def compare_configuration(self, stats: list, pos: list):
        pass

    def update_configuration(self, config: Configuration):
        pass

    def add_runresult(self, result: RunResult):
        pass

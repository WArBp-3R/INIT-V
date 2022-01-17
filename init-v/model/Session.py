from ModelInterface import ModelInterface
from network.NetworkTopology import NetworkTopology
from Configuration import Configuration
from RunResult import RunResult


class Session(ModelInterface):
    """Implements ModelInterface. Represents an INIT-V session. There always exists one session per program instance.
    A session can only have one PCAP associated with it.
    When loading a PCAP it either replaces the current PCAP of the session or a new program instance starts.
    The Session class keeps track of the current configuration,
    the preprocessor runs ,and it provides methods to save runs and update the view."""

    def __init__(self, PCAP_PATH: str, protocols: dict, run_results: list, active_config: Configuration,
                 topology: NetworkTopology):
        """The constructor of the class."""
        self.PCAP_PATH = PCAP_PATH
        """The directory of the PCAP file of the session."""
        self.protocols = protocols
        """A mapping of names of the protocols used in the
        communication in the packets of the Session's PCAP file to
        unique identification numbers."""
        self.run_results = run_results
        """A list of the run results that were calculated in the session. 
        The list is ordered in a descending order of the timestamp attribute of the RunResult list items."""
        self.active_config = active_config
        """The active configuration of the session."""
        self.topology = topology
        """The network topology which consists of the devices and connections of the Session's PCAP file."""

    def push_performance(self, pca: list, autoencoder: History):
        """Pushes the changes in the performance model to the view."""
        pass

    def push_methods(self, pca_result: list, autoencoder_result: list):
        """Pushes the changes in the method results model to the view."""
        pass

    def push_topology(self, topology: NetworkTopology):
        """Pushes the changes in the topology model to the view."""
        pass

    def push_statistics(self, stats: list):
        """Pushes the changes in the statistics model to the view."""
        pass

    def push_configuration(self, config: Configuration):
        """Pushes the changes in the configuration model to the view."""
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
        self.run_results.append(result)

from ModelInterface import ModelInterface
from network.NetworkTopology import NetworkTopology
from Configuration import Configuration
from RunResult import RunResult
from view.ViewInterface import ViewInterface


class Session(ModelInterface):
    """Implements ModelInterface. Represents an INIT-V session. There always exists one session per program instance.
    A session can only have one PCAP associated with it.
    When loading a PCAP it either replaces the current PCAP of the session or a new program instance starts.
    The Session class keeps track of the current configuration,
    the preprocessor runs ,and it provides methods to save runs and update the view."""

    def __init__(self, PCAP_PATH: str, protocols: dict, run_results: list[RunResult], active_config: Configuration,
                 topology: NetworkTopology, view: ViewInterface):
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
        self.view = view
        """A object implementing the ViewInterface interface."""

    def push_performance(self):
        """Pushes the changes in the performance model to the view."""
        self.view.update_performance(self.run_results[-1].analysis.get_pca(),
                                     self.run_results[-1].analysis.get_autoencoder())

    def push_methods(self):
        """Pushes the changes in the method results model to the view."""
        self.view.update_methods(self.run_results[-1].result.get_pca_result(),
                                 self.run_results[-1].result.get_autoencoder_result())

    def push_topology(self):
        """Pushes the changes in the topology model to the view."""
        self.view.update_topology(self.topology)

    def push_statistics(self):
        """Pushes the changes in the statistics model to the view."""
        self.view.update_statistics(self.run_results[-1].statistics.stats)

    def push_configuration(self):
        """Pushes the changes in the configuration model to the view."""
        self.view.update_configuration(self.active_config)

    def compare_performance(self, pos: list):
        """Pushes the performance information used in the compare window."""
        self.view.update_compare_performance(self.run_results, pos)

    def compare_methods(self, pos: list):
        """Pushes the run result information used in the compare window."""
        self.view.update_compare_methods(self.run_results, pos)

    def compare_statistics(self, pos: list):
        """Pushes the statistics information used in the compare window."""
        self.view.update_compare_statistics(self.run_results, pos)

    def compare_configuration(self, pos: list):
        """Pushes the configuration information in the compare window."""
        self.view.update_compare_configuration(self.run_results, pos)

    def update_configuration(self, config: Configuration):
        """Updates the active configuration."""
        self.active_config = config
        self.push_configuration()

    def add_run_result(self, result: RunResult):
        """Adds a run result to the end of the list of run results."""
        self.run_results.append(result)

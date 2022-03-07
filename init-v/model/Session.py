from model.ModelInterface import ModelInterface
from model.network.NetworkTopology import NetworkTopology
from model.Configuration import Configuration
from model.RunResult import RunResult
from model.Statistics import Statistics


class Session(ModelInterface):
    """Implements ModelInterface. Represents an INIT-V session. There always exists one session per program instance.
    A session can only have one PCAP associated with it.
    When loading a PCAP it either replaces the current PCAP of the session or a new program instance starts.
    The Session class keeps track of the current configuration,
    the preprocessor runs ,and it provides methods to save runs and update the view."""

    def __init__(self, pcap_path: str, protocols: set[str], highest_protocols: set[str], run_results: list[RunResult],
                 active_config: Configuration, topology: NetworkTopology, statistics: Statistics):
        """The constructor of the class."""
        self.pcap_path = pcap_path
        """The directory of the PCAP file of the session."""
        self.protocols = protocols
        """A mapping of names of the protocols used in the
        communication in the packets of the Session's PCAP file to
        unique identification numbers."""
        self.highest_protocols = highest_protocols
        """ The list of the highest layer protocol of each packet."""
        self.run_results = run_results
        """A list of the run results that were calculated in the session. 
        The list is ordered in a descending order of the timestamp attribute of the RunResult list items."""
        self.active_config = active_config
        """The active configuration of the session."""
        self.topology = topology
        """The network topology which consists of the devices and connections of the Session's PCAP file."""
        self.statistics: Statistics = statistics
        """Statistics of the sessions network topology."""

    def update_configuration(self, config: Configuration):
        """Updates the active configuration."""
        self.active_config = config

    def add_run_result(self, result: RunResult):
        """Adds a run result to the end of the list of run results."""
        self.run_results.append(result)

from Configuration import Configuration
from MethodResult import MethodResult
from Statistics import Statistics
from PerformanceResult import PerformanceResult
from datetime import datetime


class RunResult:
    """A result of a PCA and/or autoencoder analysis of the PCAP file and the performance analysis of it.
    It contains the results, performance and statistics of the run.
    In order to distinguish a result from another, the timestamp and configuration of the run are saved.
    """

    def __init__(self, timestamp: datetime, config: Configuration, result: MethodResult, statistics: Statistics,
                 analysis: PerformanceResult):
        """The constructor of the class."""
        self.timestamp = timestamp
        """The timestamp when the PCAP file analysis was started."""
        self.config = config
        """The configuration that was used for the PCAP file analysis."""
        self.result = result
        """The results of the calculation."""
        self.statistics = statistics
        """Miscellaneous statistics of the run and session."""
        self.analysis = analysis
        """The performance analysis of the autoencoder and/or PCA analysis of the PCAP file."""

from model.IStatistic import IStatistic


class Statistics:
    """Useful and interesting information about the PCAP and the Network."""

    def __init__(self, stats: list[IStatistic]):
        """The Constructor of the class."""
        self.stats = stats
        """List of the Statistics."""

    def get_statistics(self) -> list[IStatistic]:
        """Getter for the statistics."""
        return self.stats

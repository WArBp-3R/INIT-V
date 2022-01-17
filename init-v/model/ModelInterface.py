from network.NetworkTopology import NetworkTopology
from Configuration import Configuration
from RunResult import RunResult


class ModelInterface:
    """Interface for accessing the model package."""

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
        pass

from Configuration import Configuration
from RunResult import RunResult


class ModelInterface:
    """Interface for accessing the model package. Provides methods to push changes to the view."""

    def push_performance(self):
        """Pushes the changes in the performance model to the view."""
        pass

    def push_methods(self):
        """Pushes the changes in the method results model to the view."""
        pass

    def push_topology(self):
        """Pushes the changes in the topology model to the view."""
        pass

    def push_statistics(self):
        """Pushes the changes in the statistics model to the view."""
        pass

    def push_configuration(self):
        """Pushes the changes in the configuration model to the view."""
        pass

    def compare_performance(self, pos: list):
        """Pushes the performance information used in the compare window."""
        pass

    def compare_methods(self, pos: list):
        """Pushes the run result information used in the compare window."""
        pass

    def compare_statistics(self, pos: list):
        """Pushes the statistics information used in the compare window."""
        pass

    def compare_configuration(self, pos: list):
        """Pushes the configuration information in the compare window."""
        pass

    def update_configuration(self, config: Configuration):
        """Updates the active configuration."""
        pass

    def add_run_result(self, result: RunResult):
        """Adds a run result to the end of the list of run results."""
        pass

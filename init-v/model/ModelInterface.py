from Configuration import Configuration
from RunResult import RunResult


class ModelInterface:
    """Interface for accessing the model package. Provides methods to push changes to the view."""

    def update_configuration(self, config: Configuration):
        """Updates the active configuration."""
        pass

    def add_run_result(self, result: RunResult):
        """Adds a run result to the end of the list of run results."""
        pass

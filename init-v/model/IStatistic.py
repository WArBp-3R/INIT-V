from plotly.graph_objects import Figure


class IStatistic:
    """Interface for a statistics that can be shown in the statistics panel."""

    def get_name(self) -> str:
        """Returns the name of the statistic."""
        pass

    def get_figure(self) -> Figure:
        """Returns the graph, diagram or figure of the statistic."""
        pass

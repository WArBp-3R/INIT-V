import plotly.graph_objs as go


class Statistics:
    """Useful and interesting information about the PCAP and the Network."""

    def __init__(self):
        self.statistics: dict[str, go.Figure] = dict()

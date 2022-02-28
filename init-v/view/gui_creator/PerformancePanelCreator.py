import dash_core_components as dcc
from dash.dependencies import Output, Input

from .PanelCreator import PanelCreator

from ..GUI_Handler import get_input_id, aux_graph_toggle


class PerformancePanelCreator(PanelCreator):
    TITLE = "Performance"

    def __init__(self, handler, desc_prefix="perf", title=None):
        super().__init__(handler, desc_prefix, title)

        self.autoencoder_graph = dcc.Graph(id=self.panel.format_specifier("autoencoder_graph"))
        self.pca_graph = dcc.Graph(id=self.panel.format_specifier("pca_graph"))

        graph_ids = [self.panel.format_specifier(x) for x in ["autoencoder_graph", "pca_graph"]]
        self.graph_outputs = [Output(g, "figure") for g in graph_ids]
        self.graph_style_outputs = [Output(g, "style") for g in graph_ids]

        self.define_callbacks()

    def generate_menu(self):
        pass

    def generate_content(self):
        content = self.panel.content
        content.components = [self.autoencoder_graph, self.pca_graph]
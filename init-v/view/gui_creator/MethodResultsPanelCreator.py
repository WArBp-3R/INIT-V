import dash_core_components as dcc
from dash.dependencies import Output

from .PanelCreator import PanelCreator


class MethodResultsPanelCreator(PanelCreator):
    TITLE = "Method Results"

    def __init__(self, desc_prefix="m-res"):
        super().__init__(desc_prefix)
        self.autoencoder_graph: dcc.Graph
        self.pca_graph: dcc.Graph
        self.merged_graph: dcc.Graph
        self.active_protocols: dcc.Checklist
        self.graph_outputs: list[Output]
        self.graph_style_outputs: list[Output]

    def generate_menu(self):
        pass
        # TODO

    def generate_content(self):
        pass
        # TODO

    # callback
    def toggle_method_results_graphs(self, btn):
        pass
        # TODO

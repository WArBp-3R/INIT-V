import dash_core_components as dcc
from dash.dependencies import Output

from .PanelCreator import PanelCreator


class PerformancePanelCreator(PanelCreator):
    TITLE = "Performance"

    def __init__(self, desc_prefix="perf"):
        super().__init__(desc_prefix)
        self.autoencoder_graph = None
        self.pca_graph = None
        self.merged_graph = None
        self.active_protocols = None
        self.graph_outputs = None
        self.graph_style_outputs = None

    def generate_menu(self):
        perf_menu = self.panel.get_menu()
        perf_menu.add_menu_item("merge", "Merge")
        perf_menu.add_menu_item("show-hide", "Show/Hide").set_dropdown()

    def generate_content(self):
        pass
        # TODO

    # TODO - callback
    def toggle_perf_results_graphs(self, btn):
        pass

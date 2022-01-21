import dash_core_components as dcc
from dash.dependencies import Output

from .PanelCreator import PanelCreator


class MethodResultsPanelCreator(PanelCreator):
    TITLE = "Method Results"

    def __init__(self, desc_prefix="m-res"):
        super().__init__(desc_prefix)
        self.autoencoder_graph = None
        self.pca_graph = None
        self.merged_graph = None
        self.active_protocols = None
        self.graph_outputs = None
        self.graph_style_outputs = None

    def generate_menu(self):
        m_res_menu = self.panel.get_menu()
        m_res_menu.add_menu_item("merge", "Merge")
        m_res_menu.add_menu_item("protocol", "Protocols").set_dropdown()

    # TODO
    def generate_content(self):
        content = self.panel.content

    # TODO - callback
    def toggle_method_results_graphs(self, btn):
        pass


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
        m_res_menu.add_menu_item("protocols", "Protocols").set_dropdown()

    def generate_content(self):
        content = self.panel.content

        self.autoencoder_graph = dcc.Graph(id=self.panel.format_specifier("autoencoder_graph"))
        self.pca_graph = dcc.Graph(id=self.panel.format_specifier("pca_graph"))
        self.merged_graph = dcc.Graph(id=self.panel.format_specifier("merged_graph"))

        graphs = [self.autoencoder_graph, self.pca_graph, self.merged_graph]
        content.components = graphs

        # redefine outputs
        self.graph_outputs = [Output(g, "figure") for g in graphs]  # TODO - decide graph types and plotting methods
        self.graph_style_outputs = [Output(g, "style") for g in graphs]

        # TODO - get protocols from view interface(?)
        self.active_protocols = dcc.Checklist(id=self.panel.format_specifier("active_protocols"),
                                              options=[
                                                  {"label": "protocol placeholder1", "value": "P"},
                                                  {"label": "TCP", "value": "TCP"},
                                                  {"label": "PROFINET", "value": "PROFINET"}
                                              ])

        protocol_list_content = self.panel.get_menu()["protocols"].dropdown.set_content()
        protocol_list_content.components = [self.active_protocols]

    # TODO - callback
    def toggle_method_results_graphs(self, btn):
        pass

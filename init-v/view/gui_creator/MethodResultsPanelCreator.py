import dash_core_components as dcc
from dash.dependencies import Output, Input

from .PanelCreator import PanelCreator

from ..GUI_Handler import app, get_input_id

class MethodResultsPanelCreator(PanelCreator):
    TITLE = "Method Results"

    def __init__(self, handler, desc_prefix="m-res", title=None):
        super().__init__(handler, desc_prefix, title)
        self.autoencoder_graph = None
        self.pca_graph = None
        self.merged_graph = None
        self.active_protocols = None
        self.graph_outputs = []
        self.graph_style_outputs = []

        self.define_callbacks()

    def define_callbacks(self):
        app.callback(
            Output(self.panel.format_specifier("autoencoder_graph"), "style"),
            Output(self.panel.format_specifier("pca_graph"), "style"),
            Output(self.panel.format_specifier("merged_graph"), "style"),
            Input(self.panel.get_menu()["merge"].id, "n_clicks")
        )(self.toggle_method_results_graphs)

        app.callback(
            Output(self.panel.format_specifier("active_protocols"), "options"),
            Output(self.panel.get_menu()["protocols"].dropdown.id, "style"),
            Input(self.panel.get_menu()["protocols"].btn.id, "n_clicks"),
        )(self.update_protocols)

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
        graph_ids = ["autoencoder_graph, pca_graph", "merged_graph"]
        content.components = graphs

        # redefine outputs
        self.graph_outputs = [Output(g, "figure") for g in graph_ids]  # TODO - decide graph types and plotting methods
        self.graph_style_outputs = [Output(g, "style") for g in graph_ids]

        # TODO - get protocols from view interface(?)
        self.active_protocols = dcc.Checklist(id=self.panel.format_specifier("active_protocols"))

        protocol_list_content = self.panel.get_menu()["protocols"].dropdown.set_content()
        protocol_list_content.components = [self.active_protocols]

    # TODO - fix init
    def toggle_method_results_graphs(self, btn):
        print("toggle_method_results_graphs")
        enabled = {"display": "flex"}
        disabled = {"display": "none"}
        if btn % 2 == 1:
            return disabled, disabled, enabled
        else:
            return enabled, enabled, disabled

    # TODO - replace stub (WIP)
    def update_protocols(self, btn):
        button_id = get_input_id()
        print("update_protocols")
        # view adapter stuff
        protocol_options = [{"label": "protocol placeholder1", "value": "P"},
                            {"label": "TCP", "value": "TCP"},
                            {"label": "PROFINET", "value": "PROFINET"}, ]
        style_result = {"display": "none"}
        if button_id == self.panel.get_menu()["protocols"].btn.id:
            if btn % 2 == 1:
                style_result = {"display": "flex"}
        else:
            pass
        return protocol_options, style_result

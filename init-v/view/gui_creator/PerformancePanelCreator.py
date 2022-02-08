import dash_core_components as dcc
from dash.dependencies import Output, Input

from .PanelCreator import PanelCreator

from ..GUI_Handler import app, get_input_id

class PerformancePanelCreator(PanelCreator):
    TITLE = "Performance"

    def __init__(self, handler, desc_prefix="perf", title=None):
        super().__init__(handler, desc_prefix, title)
        self.autoencoder_graph = dcc.Graph(id=self.panel.format_specifier("autoencoder_graph"))
        self.pca_graph = dcc.Graph(id=self.panel.format_specifier("pca_graph"))
        self.merged_graph = dcc.Graph(id=self.panel.format_specifier("merged_graph"))
        self.active_protocols = dcc.Checklist(id=self.panel.format_specifier("active_protocols"))

        graph_ids = [self.panel.format_specifier(x) for x in ["autoencoder_graph", "pca_graph", "merged_graph"]]
        self.graph_outputs = [Output(g, "figure") for g in graph_ids]  # TODO - decide graph types and plotting methods
        self.graph_style_outputs = [Output(g, "style") for g in graph_ids]

        self.define_callbacks()

    def define_callbacks(self):
        app.callback(
            Output(self.panel.format_specifier("autoencoder_graph"), "style"),
            Output(self.panel.format_specifier("pca_graph"), "style"),
            Output(self.panel.format_specifier("merged_graph"), "style"),
            Input(self.panel.get_menu()["merge"].id, "n_clicks")
        )(self.toggle_perf_results_graphs)

    def generate_menu(self):
        perf_menu = self.panel.get_menu()
        perf_menu.add_menu_item("merge", "Merge")
        perf_menu.add_menu_item("show-hide", "Show/Hide").set_dropdown()

    def generate_content(self):
        content = self.panel.content

        content.components = [self.autoencoder_graph, self.pca_graph, self.merged_graph]

        self.accuracy = dcc.Checklist(id=self.panel.format_specifier("accuracy"),
                                      options=[
                                          {"label": "Training Accuracy", "value": "training"},
                                          {"label": "Validation Accuracy", "value": "validation"},
                                          {"label": "Test Accuracy", "value": "test"}
                                      ],
                                      value=[])

        self.data_loss = dcc.Checklist(id=self.panel.format_specifier("data_loss"),
                                       options=[
                                           {"label": "Loss on the Train Data", "value": "train"},
                                           {"label": "Loss on the Test Data", "value": "test"}
                                       ],
                                       value=[])

        protocol_list_content = self.panel.get_menu()["show-hide"].dropdown.set_content()
        protocol_list_content.components = [
            "Autoencoder",
            self.accuracy,
            "PCA",
            self.data_loss
        ]

    # TODO - fix init
    def toggle_perf_results_graphs(self, btn):
        print("toggle_perf_results_graphs")
        enabled = {"display": "flex"}
        disabled = {"display": "none"}

        button_id = get_input_id()
        if button_id == self.panel.get_menu()["merge"].id:
            if btn % 2 == 1:
                return disabled, disabled, enabled
            else:
                return enabled, enabled, disabled
        else:
            return enabled, enabled, disabled

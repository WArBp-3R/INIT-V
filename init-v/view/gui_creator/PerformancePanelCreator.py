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
        self.accuracy = None
        self.data_loss = None
        self.graph_outputs = None
        self.graph_style_outputs = None

    def generate_menu(self):
        perf_menu = self.panel.get_menu()
        perf_menu.add_menu_item("merge", "Merge")
        perf_menu.add_menu_item("show-hide", "Show/Hide").set_dropdown()

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

        self.accuracy = dcc.Checklist(id="accuracy",
                                      options=[
                                          {"label": "Training Accuracy", "value": "training"},
                                          {"label": "Validation Accuracy", "value": "validation"},
                                          {"label": "Test Accuracy", "value": "test"}
                                      ])

        self.data_loss = dcc.Checklist(id="data_loss",
                                       options=[
                                           {"label": "Loss on the Train Data", "value": "train"},
                                           {"label": "Loss on the Test Data", "value": "test"}
                                       ])

        protocol_list_content = self.panel.get_menu()["show-hide"].dropdown.set_content()
        protocol_list_content.components = [
            "Autoencoder",
            self.accuracy,
            "PCA",
            self.data_loss
        ]

    # TODO - callback
    def toggle_perf_results_graphs(self, btn):
        pass

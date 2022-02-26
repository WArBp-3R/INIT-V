import dash_core_components as dcc
from dash.dependencies import Output, Input

from .PanelCreator import PanelCreator

class MethodResultsPanelCreator(PanelCreator):
    TITLE = "Method Results"

    def __init__(self, handler, desc_prefix="m-res", title=None):
        super().__init__(handler, desc_prefix, title)

        self.autoencoder_graph = dcc.Graph(id=self.panel.format_specifier("autoencoder_graph"))
        self.pca_graph = dcc.Graph(id=self.panel.format_specifier("pca_graph"))
        self.merged_graph = dcc.Graph(id=self.panel.format_specifier("merged_graph"))

        graph_ids = [self.panel.format_specifier(x) for x in ["autoencoder_graph", "pca_graph", "merged_graph"]]
        self.graph_outputs = [Output(g, "figure") for g in graph_ids]
        self.graph_style_outputs = [Output(g, "style") for g in graph_ids]

        self.define_callbacks()

    def generate_menu(self):
        m_res_menu = self.panel.get_menu()
        m_res_menu.add_menu_item("merge", "Merge")

    def generate_content(self):
        content = self.panel.content
        content.components = [self.autoencoder_graph, self.pca_graph, self.merged_graph]

    def define_callbacks(self):
        super().define_callbacks()

        enabled = {"display": "flex"}
        disabled = {"display": "none"}

        self.handler.cb_mgr.register_callback(
            self.graph_style_outputs,
            Input(self.panel.get_menu()["merge"].id, "n_clicks"),
            lambda x: [disabled, disabled, enabled] if x % 2 == 1 else [enabled, enabled, disabled],
            default_outputs=[enabled, enabled, disabled]
        )

import dash_core_components as dcc
from dash.dependencies import Output

import plotly.express as px

from .PanelCreator import PanelCreator


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

    # CALLBACK METHODS
    def update_performance_panel(self, run_id):
        ae_fig = None
        pca_fig = None

        ae_data, pca_data = self.handler.interface.get_performance(run_id)

        if len(ae_data.history) > 0:
            ae_df = dict()
            ae_df["epoch"] = []
            ae_df["loss/accuracy"] = []
            ae_df["keys"] = []
            for k in ae_data.history.keys():
                ae_df["epoch"] += ae_data.epoch
                ae_df["loss/accuracy"] += ae_data.history[k]
                ae_df["keys"] += [k for k in range(0, len(ae_data.epoch))]

            ae_fig = px.line(ae_df, x="epoch", y="loss/accuracy", color="keys", markers=True)

        if pca_data:
            pca_df = dict()
            pca_df["y"] = pca_data
            pca_df["x"] = ["Training Data", "Test Data"]

            pca_fig = px.bar(pca_df, x="x", y="y")

        return ae_fig, pca_fig

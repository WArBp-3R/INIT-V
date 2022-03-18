import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Output

from .PanelCreator import PanelCreator


class PerformancePanelCreator(PanelCreator):
    TITLE = "Performance"

    def __init__(self, handler, desc_prefix="perf"):
        self.autoencoder_graph = None
        self.pca_result = None

        # Dash Dependencies
        self.result_outputs = None

        super().__init__(handler, desc_prefix)

    def generate_menu(self):
        pass

    def generate_content(self):
        self.autoencoder_graph = dcc.Graph(id=self.panel.format_specifier("autoencoder_graph"))
        self.pca_result = html.Div(id=self.panel.format_specifier("pca_result"))
        self.result_outputs = [Output(self.autoencoder_graph.id, "figure"), Output(self.pca_result.id, "children")]

        self.panel.content.components = [self.autoencoder_graph, self.pca_result]

    # CALLBACK METHODS
    def update_performance_panel(self, run_id):
        run_id = int(run_id)
        if len(self.handler.interface.get_run_list()) == 0:
            return None

        ae_fig = None
        pca_result = None

        ae_data, pca_data = self.handler.interface.get_performance(run_id)

        if ae_data and len(ae_data) > 0:
            ae_df = dict()
            ae_df["epoch"] = []
            ae_df["loss/accuracy"] = []
            ae_df["keys"] = []
            for k in ae_data.keys():
                epoch_number_list = range(0, len(ae_data[k]))
                ae_df["epoch"] += epoch_number_list
                ae_df["loss/accuracy"] += ae_data[k]
                ae_df["keys"] += [k for i in epoch_number_list]

            ae_fig = px.line(ae_df, x="epoch", y="loss/accuracy", color="keys", markers=True, title="Autoencoder",
                             template="plotly_dark")

        if pca_data:
            pca_result = [
                html.H3("PCA"),
                html.P(f"Training Data: {pca_data[0]}"),
                html.P(f"Test Data: {pca_data[1]}"),
                html.P(f"Delta: {pca_data[0] - pca_data[1]}")
            ]

        return [ae_fig, pca_result]

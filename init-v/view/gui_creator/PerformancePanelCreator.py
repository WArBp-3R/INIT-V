import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Output

from .PanelCreator import PanelCreator


class PerformancePanelCreator(PanelCreator):
    TITLE = "Performance"

    def __init__(self, handler, desc_prefix="perf"):
        self.autoencoder_graph = None
        self.pca_result_tbody = None
        self.pca_result_table = None
        self.pca_div = None

        # Dash Dependencies
        self.result_outputs = None

        super().__init__(handler, desc_prefix)

    def generate_menu(self):
        pass

    def generate_content(self):
        temp = {"resx": {"title": "x"}, "resy": {"title": "y"}}
        fig = px.scatter(temp, x="resx", y="resy", title='run to create graph', template="plotly_dark")
        self.autoencoder_graph = dcc.Graph(figure=fig, id=self.panel.format_specifier("autoencoder_graph"))
        self.pca_result_tbody = html.Tbody(id=self.panel.format_specifier("pca_result_tbody"))
        self.pca_result_table = html.Table(id=self.panel.format_specifier("pca_result_table"),
                                           children=[
                                               html.Thead(children=[
                                                   html.Tr(children=[
                                                       html.Th("#ID"),
                                                       html.Th("Training Data"),
                                                       html.Th("Testing Data"),
                                                       html.Th("Delta"),
                                                   ])
                                               ]),
                                               self.pca_result_tbody
                                           ])
        self.pca_div = html.Div(id=self.panel.format_specifier("pca_result"),
                                children=[html.H3("PCA"), self.pca_result_table])

        self.result_outputs = [Output(self.autoencoder_graph.id, "figure"),
                               Output(self.pca_result_tbody.id, "children")]

        self.panel.content.components = [self.autoencoder_graph, self.pca_div]

    # CALLBACK METHODS
    def update_performance_panel(self, runs):
        runs = sorted(runs, reverse=True)
        if len(self.handler.interface.get_run_list()) == 0:
            return None

        result_list = self.handler.interface.get_performance(runs)
        ae_main_df = {
            "run": list(), "epoch": list(), "loss/accuracy": list(), "keys": list()
        }
        pca_main_df = list()

        for res, run in zip(result_list, runs):
            ae_data, pca_data = res[0], res[1]

            ae_df = dict()
            if ae_data and len(ae_data) > 0:
                ae_df["run"] = ae_main_df["run"]
                ae_df["epoch"] = ae_main_df["epoch"]
                ae_df["loss/accuracy"] = ae_main_df["loss/accuracy"]
                ae_df["keys"] = ae_main_df["keys"]
                for k in ae_data.keys():
                    epoch_number_list = range(0, len(ae_data[k]))
                    ae_df["run"] += [run for i in epoch_number_list]
                    ae_df["epoch"] += epoch_number_list
                    ae_df["loss/accuracy"] += ae_data[k]
                    ae_df["keys"] += [k for i in epoch_number_list]
                ae_main_df.update(ae_df)

            pca_df = dict()
            if pca_data:
                pca_df["run"] = run
                pca_df["train"] = pca_data[0]
                pca_df["test"] = pca_data[1]
                pca_df["delta"] = pca_data[0] - pca_data[1]
                pca_main_df.append(pca_df)

        ae_fig = px.line(ae_main_df, x="epoch", y="loss/accuracy", color="run", symbol="keys", markers=True,
                         title="Autoencoder", template="plotly_dark")
        pca_result = [
            html.Tr(children=[
                html.Td(df["run"]),
                html.Td(df["train"]),
                html.Td(df["test"]),
                html.Td(df["delta"])
            ]) for df in pca_main_df
        ]

        return [ae_fig, pca_result]

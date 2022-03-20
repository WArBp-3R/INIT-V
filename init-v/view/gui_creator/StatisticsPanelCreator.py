import dash_core_components as dcc
from dash.dependencies import Output, Input
import plotly.express as px
from .PanelCreator import PanelCreator


class StatisticsPanelCreator(PanelCreator):
    TITLE = "Statistics"

    def __init__(self, handler, desc_prefix="stats"):
        self.stats_list = None
        self.stat_graph = None

        super().__init__(handler, desc_prefix)

    def generate_menu(self):
        stats_menu = self.panel.get_menu()
        stats_dd = stats_menu.add_menu_item("stats_dd", "Stats List").set_dropdown()
        stats_dd.set_content()

    def generate_content(self):
        temp = {"statx": {"title": "x"}, "staty": {"title": "y"}}
        self.stats_list = dcc.RadioItems(id=self.panel.format_specifier("stats_list"))
        self.stat_graph = dcc.Graph(figure=px.scatter(temp,
                                                      x="statx", y="staty", title='Please choose a statistic',
                                                      template="plotly_dark"),
                                    id=self.panel.format_specifier("stat_graph"))

        self.panel.content.components = [self.stat_graph]

        stats_list_content = self.panel.get_menu()["stats_dd"].dropdown.set_content()
        stats_list_content.components = [self.stats_list]

    def define_callbacks(self):
        super().define_callbacks()
        temp = {"loss/accuracy": {"title": "loss/accuracy"}, "epoch": {"title": "epoch"}}
        self.handler.cb_mgr.register_callback(
            [Output(self.stat_graph.id, "figure")],
            Input(self.stats_list.id, "value"),
            lambda v: [self.handler.interface.get_statistics().statistics[v]],
            default_outputs=[px.scatter(temp, x="loss/accuracy", y="epoch", title='Autoencoder', template="plotly_dark")]
        )

    # CALLBACKS
    def update_stats_list(self, btn):
        stats_options = []
        stats_names = self.handler.interface.get_statistics().statistics.keys()
        for s in stats_names:
            stats_options.append({"label": s, "value": s})

        return [stats_options]

import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Output, Input

from .PanelCreator import PanelCreator
from ..utility.MethodResultContainer import MethodResultContainer, merge_result_containers


class MethodResultsPanelCreator(PanelCreator):
    TITLE = "Method Results"

    def __init__(self, handler, desc_prefix="m-res"):
        self.autoencoder_graph = None
        self.pca_graph = None
        self.merged_graph = None

        # Dash Dependencies
        self.graph_outputs = None
        self.graph_style_outputs = None

        super().__init__(handler, desc_prefix)

    def generate_menu(self):
        m_res_menu = self.panel.get_menu()
        m_res_menu.add_menu_item("merge", "Merge")

    def generate_content(self):
        temp = {"resx": {"title": "x"}, "resy": {"title": "y"}}
        fig = px.scatter(temp, x="resx", y="resy", title='run to create graph', template="plotly_dark")
        self.autoencoder_graph = dcc.Graph(figure=fig, id=self.panel.format_specifier("autoencoder_graph"))
        self.pca_graph = dcc.Graph(figure=fig, id=self.panel.format_specifier("pca_graph"))
        self.merged_graph = dcc.Graph(figure=fig, id=self.panel.format_specifier("merged_graph"))

        graphs = [self.autoencoder_graph, self.pca_graph, self.merged_graph]
        self.graph_outputs = [Output(g.id, "figure") for g in graphs]
        self.graph_style_outputs = [Output(g.id, "style") for g in graphs]

        self.panel.content.components = graphs

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

    # CALLBACK METHODS
    def update_method_results_panel(self, runs):
        runs = sorted(runs, reverse=True)
        if len(self.handler.interface.get_run_list()) == 0:
            return None

        result_list = self.handler.interface.get_method_results(runs)
        ae_main_df = dict()
        pca_main_df = dict()
        merged_main_df = dict()

        hover_data_keys = None

        for res, run in zip(result_list, runs):
            ae_data, pca_data = res[0], res[1]

            ae_data_exists = ae_data and len(ae_data) > 0
            pca_data_exists = pca_data and len(pca_data) > 0

            ae_container = None
            if ae_data_exists:
                ae_packet_mappings = [(d[0], d[1]) for d in ae_data]
                ae_hover_information = [d[2] for d in ae_data]
                ae_highest_protocols = [d[3] for d in ae_data]
                ae_container = MethodResultContainer(run, ae_packet_mappings, ae_highest_protocols,
                                                     ae_hover_information)
                if not hover_data_keys:
                    hover_data_keys = ae_container.hover_data[0].keys()

                for k in ae_container.packet_figure_dict.keys():
                    if k not in ae_main_df.keys():
                        ae_main_df[k] = list()
                    ae_main_df[k] += ae_container.packet_figure_dict[k]

            pca_container = None
            if pca_data_exists:
                pca_packet_mappings = [(d[0], d[1]) for d in pca_data]
                pca_hover_information = [d[2] for d in pca_data]
                pca_highest_protocols = [d[3] for d in pca_data]
                pca_container = MethodResultContainer(run, pca_packet_mappings, pca_highest_protocols,
                                                      pca_hover_information)
                if not hover_data_keys:
                    hover_data_keys = pca_container.hover_data[0].keys()

                for k in pca_container.packet_figure_dict.keys():
                    if k not in pca_main_df.keys():
                        pca_main_df[k] = list()
                    pca_main_df[k] += pca_container.packet_figure_dict[k]

            merged_container = None
            merged_results = [] + ([ae_container] if ae_data_exists else []) + (
                [pca_container] if pca_data_exists else [])
            merged_titles = [] + (["Autoencoder"] if ae_data_exists else []) + (["PCA"] if pca_data_exists else [])
            merged_container = merge_result_containers(run, merged_results, merged_titles)

            for k in merged_container.packet_figure_dict.keys():
                if k not in merged_main_df.keys():
                    merged_main_df[k] = list()
                merged_main_df[k] += merged_container.packet_figure_dict[k]

        ae_fig = px.scatter(ae_main_df, x="x", y="y", color="run", symbol="protocols",
                            hover_data=hover_data_keys, title="Autoencoder",
                            template="plotly_dark") if ae_main_df else dict()
        pca_fig = px.scatter(pca_main_df, x="x", y="y", color="run", symbol="protocols",
                             hover_data=hover_data_keys, title="PCA", template="plotly_dark") if pca_main_df else dict()
        merged_fig = px.scatter(merged_main_df, x="x", y="y", color="run", symbol="protocols",
                                hover_data=hover_data_keys,
                                title=f"{'Autoencoder' if ae_main_df else ''} {'+' if ae_main_df and pca_main_df else ''} {'PCA' if pca_main_df else ''} (merged)" if merged_main_df else dict(),
                                template="plotly_dark")

        return [ae_fig, pca_fig, merged_fig]

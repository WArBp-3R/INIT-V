import dash_core_components as dcc
from dash.dependencies import Output, Input
import plotly.express as px
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
        self.merged_graph = dcc.Graph(id=self.panel.format_specifier("merged_graph"))

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
    def update_method_results_panel(self, run_id):
        run_id = int(run_id)
        if len(self.handler.interface.get_run_list()) == 0:
            return None

        ae_data, pca_data = self.handler.interface.get_method_results(run_id)

        ae_data_exists = ae_data and len(ae_data) > 0
        pca_data_exists = pca_data and len(pca_data) > 0

        ae_container = None
        if ae_data_exists:
            ae_packet_mappings = [(d[0], d[1]) for d in ae_data]
            ae_hover_information = [d[2] for d in ae_data]
            ae_highest_protocols = [d[3] for d in ae_data]
            ae_container = MethodResultContainer(ae_packet_mappings, ae_highest_protocols,
                                                 ae_hover_information, title="Autoencoder")

        pca_container = None
        if pca_data_exists:
            pca_packet_mappings = [(d[0], d[1]) for d in pca_data]
            pca_hover_information = [d[2] for d in pca_data]
            pca_highest_protocols = [d[3] for d in pca_data]
            pca_container = MethodResultContainer(pca_packet_mappings, pca_highest_protocols,
                                                  pca_hover_information, title="PCA")

        merged_container = None
        if ae_data_exists and pca_data_exists:
            merged_container = merge_result_containers([ae_container, pca_container], ["Autoencoder", "PCA"])

        return [ae_container.figure if ae_container else None, pca_container.figure if pca_container else None,
                merged_container.figure if merged_container else None]

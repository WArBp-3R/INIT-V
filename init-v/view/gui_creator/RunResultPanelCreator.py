import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input

from .MethodResultsPanelCreator import MethodResultsPanelCreator
from .PanelCreator import PanelCreator
from .PerformancePanelCreator import PerformancePanelCreator


class RunResultPanelCreator(PanelCreator):
    TITLE = "Run Results"

    def __init__(self, handler, desc_prefix="run"):
        self.run_ids = None

        spc = [x(handler) for x in [MethodResultsPanelCreator, PerformancePanelCreator]]

        super().__init__(handler, desc_prefix, sub_panel_creators=spc)

    def generate_menu(self):
        run_result_menu = self.panel.get_menu()
        run_result_menu.add_menu_item("NONE", "NONE")

    def generate_content(self):
        self.run_ids = dcc.Input(id=self.panel.format_specifier("run_ids"), type="hidden", value="")

        self.panel.content.components = [self.run_ids] + [spc.panel.layout for spc in
                                                          self.sub_panel_creators.values()]

    def define_callbacks(self):
        super().define_callbacks()

        m_res_spc: MethodResultsPanelCreator = self.sub_panel_creators["m-res"]
        perf_spc: PerformancePanelCreator = self.sub_panel_creators["perf"]

        self.handler.cb_mgr.register_callback(
            m_res_spc.graph_outputs,
            Input(self.run_ids.id, "value"),
            m_res_spc.update_method_results_panel,
            default_outputs=[{"layout": {"title": "Autoencoder",
                                         "xaxis": {"title": "ex"},
                                         "yaxis": {"title": "eps"}}},
                             {"layout": {"title": "PCA",
                                         "xaxis": {"title": "ex"},
                                         "yaxis": {"title": "eps"}
                                         }},
                             {"layout": {"title": "Autoencoder + PCA",
                                         "xaxis": {"title": "ex"},
                                         "yaxis": {"title": "eps"}
                                         }}]
        )

        self.handler.cb_mgr.register_callback(
            perf_spc.result_outputs,
            Input(self.run_ids.id, "value"),
            perf_spc.update_performance_panel,
            default_outputs=[{"layout": {"title": "Autoencoder",
                                         "xaxis": {"title": "ex"},
                                         "yaxis": {"title": "eps"}
                                         }},
                             [html.H3("PCA"),
                              html.P(f"Training Data: {None}"),
                              html.P(f"Test Data: {None}"),
                              html.P(f"Delta: {None}")]]
        )

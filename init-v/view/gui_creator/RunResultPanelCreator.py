import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from .MethodResultsPanelCreator import MethodResultsPanelCreator
from .PanelCreator import PanelCreator
from .PerformancePanelCreator import PerformancePanelCreator


class RunResultPanelCreator(PanelCreator):
    TITLE = "Run Results"

    def __init__(self, handler, desc_prefix="run"):
        self.select_run_list = None
        self.run_ids = None

        spc = [x[0](handler, desc_prefix=x[1]) for x in
               [(MethodResultsPanelCreator, f"{desc_prefix}_pnl_m-res"),
                (PerformancePanelCreator, f"{desc_prefix}_pnl_perf")]]

        super().__init__(handler, desc_prefix, sub_panel_creators=spc)

    def generate_menu(self):
        run_result_menu = self.panel.get_menu()
        run_select_dd = run_result_menu.add_menu_item("select-run", "Select Run").set_dropdown()

    def generate_content(self):
        self.run_ids = dcc.Input(id=self.panel.format_specifier("run_ids"), type="hidden", value="")

        self.panel.content.components = [self.run_ids] + [spc.panel.layout for spc in
                                                          self.sub_panel_creators.values()]

        self.select_run_list = dcc.RadioItems(id=self.panel.format_specifier("select_run"))
        self.panel.get_menu()["select-run"].dropdown.set_content().components = [self.select_run_list]

    def define_callbacks(self):
        super().define_callbacks()

        m_res_spc: MethodResultsPanelCreator = self.sub_panel_creators[self.panel.format_specifier("m-res")]
        perf_spc: PerformancePanelCreator = self.sub_panel_creators[self.panel.format_specifier("perf")]

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

        self.register_dropdown_list_update_callback(self.select_run_list, "select-run", self.update_select_run_list)

        self.handler.cb_mgr.register_callback(
            [Output(self.run_ids.id, "value")],
            Input(self.select_run_list.id, "value"),
            lambda x: [x],
            default_outputs=[""]
        )

    # CALLBACK METHODS
    def update_select_run_list(self, btn):
        run_options = []
        run_names = self.handler.interface.get_run_list()
        for i in range(0, len(run_names)):
            run_options.append({"label": run_names[i], "value": str(i)})
        style_result = {"display": "flex"} if btn % 2 == 1 else {"display": "none"}
        return [run_options, style_result]

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

        spc = [x[0](handler, desc_prefix=x[1]) for x in
               [(MethodResultsPanelCreator, f"{desc_prefix}_pnl_m-res"),
                (PerformancePanelCreator, f"{desc_prefix}_pnl_perf")]]

        super().__init__(handler, desc_prefix, sub_panel_creators=spc)

    def generate_menu(self):
        run_result_menu = self.panel.get_menu()
        run_result_menu.add_menu_item("select-run", "Select Run").set_dropdown()

    def generate_content(self):
        self.panel.content.components = [html.Div(),
                                         html.Div([spc.panel.layout for spc in self.sub_panel_creators.values()])]

        self.select_run_list = dcc.Checklist(id=self.panel.format_specifier("select_run_list"))
        self.panel.get_menu()["select-run"].dropdown.set_content().components = [self.select_run_list]

    def define_callbacks(self):
        super().define_callbacks()

        m_res_spc: MethodResultsPanelCreator = self.sub_panel_creators[self.panel.format_specifier("m-res")]
        perf_spc: PerformancePanelCreator = self.sub_panel_creators[self.panel.format_specifier("perf")]

        self.handler.cb_mgr.register_callback(
            [Output(self.panel.titlebar.title.id, "children")],
            Input(self.select_run_list.id, "value"),
            lambda x: [f"{self.TITLE} - Run: {', '.join(x)}"],
            default_outputs=[self.TITLE]
        )

        # self.handler.cb_mgr.register_callback(
        #     [Output()] cfg
        # )

        # self.handler.cb_mgr.register_callback(
        #     m_res_spc.graph_outputs,
        #     Input(self.select_run_list.id, "value"),
        #     m_res_spc.update_method_results_panel,
        #     default_outputs=[{"layout": {"title": "Autoencoder",
        #                                  "xaxis": {"title": "ex"},
        #                                  "yaxis": {"title": "eps"}}},
        #                      {"layout": {"title": "PCA",
        #                                  "xaxis": {"title": "ex"},
        #                                  "yaxis": {"title": "eps"}
        #                                  }},
        #                      {"layout": {"title": "Autoencoder + PCA",
        #                                  "xaxis": {"title": "ex"},
        #                                  "yaxis": {"title": "eps"}
        #                                  }}]
        # )
        #
        # self.handler.cb_mgr.register_callback(
        #     perf_spc.result_outputs,
        #     Input(self.select_run_list.id, "value"),
        #     perf_spc.update_performance_panel,
        #     default_outputs=[{"layout": {"title": "Autoencoder",
        #                                  "xaxis": {"title": "ex"},
        #                                  "yaxis": {"title": "eps"}
        #                                  }},
        #                      [html.H3("PCA"),
        #                       html.P(f"Training Data: {None}"),
        #                       html.P(f"Test Data: {None}"),
        #                       html.P(f"Delta: {None}")]]
        # )

        # self.register_dropdown_list_update_callback(self.select_run_list, "select-run", self.update_select_run_list)

    # CALLBACK METHODS
    def update_select_run_list(self, void):
        run_options = []
        run_names = self.handler.interface.get_run_list()
        for i in range(0, len(run_names)):
            run_options.append({"label": f"{str(i)}: {run_names[i]}", "value": str(i)})
        return [run_options, [run_options[-1]["value"]]] if len(run_options) > 0 else None

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px

from .MethodResultsPanelCreator import MethodResultsPanelCreator
from .PanelCreator import PanelCreator
from .PerformancePanelCreator import PerformancePanelCreator
from .ReadOnlyConfigPanelCreator import ReadOnlyConfigPanelCreator


class RunResultPanelCreator(PanelCreator):
    TITLE = "Run Results"

    def __init__(self, handler, desc_prefix="run", title=None):
        self.select_run_list = None

        spc = [x[0](handler, desc_prefix=x[1]) for x in
               [(MethodResultsPanelCreator, f"{desc_prefix}_pnl_m-res"),
                (PerformancePanelCreator, f"{desc_prefix}_pnl_perf"),
                (ReadOnlyConfigPanelCreator, f"{desc_prefix}_pnl_ro-cfg")]]

        super().__init__(handler, desc_prefix, sub_panel_creators=spc, title=title if title else self.TITLE)

    def generate_menu(self):
        run_result_menu = self.panel.get_menu()
        run_result_menu.add_menu_item("select-run", "Select Run").set_dropdown()

    def generate_content(self):
        m_res_spc: MethodResultsPanelCreator = self.sub_panel_creators[self.panel.format_specifier("m-res")]
        perf_spc: PerformancePanelCreator = self.sub_panel_creators[self.panel.format_specifier("perf")]
        ro_cfg_spc: ReadOnlyConfigPanelCreator = self.sub_panel_creators[self.panel.format_specifier("ro-cfg")]

        self.panel.content.components = [html.Div(ro_cfg_spc.panel.layout),
                                         html.Div(children=[m_res_spc.panel.layout, perf_spc.panel.layout])]

        self.select_run_list = dcc.Checklist(id=self.panel.format_specifier("select_run_list"))
        self.panel.get_menu()["select-run"].dropdown.set_content().components = [self.select_run_list]

    def define_callbacks(self):
        super().define_callbacks()

        m_res_spc: MethodResultsPanelCreator = self.sub_panel_creators[self.panel.format_specifier("m-res")]
        perf_spc: PerformancePanelCreator = self.sub_panel_creators[self.panel.format_specifier("perf")]
        ro_cfg_spc: ReadOnlyConfigPanelCreator = self.sub_panel_creators[self.panel.format_specifier("ro-cfg")]

        self.handler.cb_mgr.register_callback(
            [Output(ro_cfg_spc.configs_tbody.id, "children")],
            Input(self.select_run_list.id, "value"),
            ro_cfg_spc.display_config,
            default_outputs=["No runs selected"]
        )

        temp = {"x": {"title": "x"}, "y": {"title": "y"}}

        self.handler.cb_mgr.register_callback(
            m_res_spc.graph_outputs,
            Input(self.select_run_list.id, "value"),
            m_res_spc.update_method_results_panel,
            default_outputs=[px.scatter(temp, x="x", y="y", title='Autoencoder', template="plotly_dark"),
                             px.scatter(temp, x="x", y="y", title='PCA', template="plotly_dark"),
                             px.scatter(temp, x="x", y="y", title='Autoencoder + PCA', template="plotly_dark")]
        )

        temp = {"loss/accuracy": {"title": "loss/accuracy"}, "epoch": {"title": "epoch"}}

        self.handler.cb_mgr.register_callback(
            perf_spc.result_outputs,
            Input(self.select_run_list.id, "value"),
            perf_spc.update_performance_panel,
            default_outputs=[px.scatter(temp, x="loss/accuracy", y="epoch", title='Autoencoder', template="plotly_dark"),
                             "No PCA results"]
        )

        # self.register_dropdown_list_update_callback(self.select_run_list, "select-run", self.update_select_run_list)

    # CALLBACK METHODS
    def update_select_run_list(self, void):
        run_options = []
        run_names = self.handler.interface.get_run_list()
        for i in range(0, len(run_names)):
            run_options.append({"label": f"{str(i)}: {run_names[i]}", "value": str(i)})
        run_options.reverse()
        return [run_options, [run_options[0]["value"]]] if len(run_options) > 0 else None

    def display_select_run_list(self, void):
        run_options = []
        run_names = self.handler.interface.get_run_list()
        for i in range(0, len(run_names)):
            run_options.append({"label": f"{str(i)}: {run_names[i]}", "value": str(i)})
        run_options.reverse()
        return [run_options] if len(run_options) > 0 else None

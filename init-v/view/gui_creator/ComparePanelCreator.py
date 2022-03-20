import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from .PanelCreator import PanelCreator
from .RunResultPanelCreator import RunResultPanelCreator


class ComparePanelCreator(PanelCreator):
    TITLE = "Compare Runs"
    IS_MAIN_PANEL = True

    def __init__(self, handler, desc_prefix="cmp"):
        spc = [x[0](handler, desc_prefix=x[1], title=x[2]) for x in
               [(RunResultPanelCreator, "run_1", "Run Results #1"), (RunResultPanelCreator, "run_2", "Run Results #2")]]

        super().__init__(handler, desc_prefix, sub_panel_creators=spc)

    def generate_menu(self):
        cmp_menu = self.panel.get_menu()
        cmp_menu.add_menu_item("dashboard", "Dashboard", "/dashboard")

        cmp_menu.add_menu_item("update-runs", "Update Runs")

    def generate_content(self):
        content = self.panel.content
        content.components = [spc.panel.layout for spc in self.sub_panel_creators.values()]

    def define_callbacks(self):
        super().define_callbacks()

        run_1_spc: RunResultPanelCreator = self.sub_panel_creators["run_1"]
        run_2_spc: RunResultPanelCreator = self.sub_panel_creators["run_2"]

        for spc in [run_1_spc, run_2_spc]:
            self.handler.cb_mgr.register_multiple_callbacks(
                [Output(spc.select_run_list.id, "options")], {
                    Input(self.panel.get_menu()["update-runs"].id, "n_clicks"): (
                        spc.display_select_run_list, None),
                },
                [[{"label": "Click update runs in menu to load runs", "value": ""}]]
            )

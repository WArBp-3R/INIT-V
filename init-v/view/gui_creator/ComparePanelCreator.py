import dash_core_components as dcc
import dash_html_components as html

from .PanelCreator import PanelCreator
from .RunResultPanelCreator import RunResultPanelCreator


class ComparePanelCreator(PanelCreator):
    TITLE = "Compare Runs"
    IS_MAIN_PANEL = True

    def __init__(self, handler, desc_prefix="cmp"):
        spc = [x[0](handler, desc_prefix=x[1]) for x in
               [(RunResultPanelCreator, "run_1"), (RunResultPanelCreator, "run_2")]]

        super().__init__(handler, desc_prefix, sub_panel_creators=spc)

    def generate_menu(self):
        cmp_menu = self.panel.get_menu()
        cmp_menu.add_menu_item("dashboard", "Dashboard", "/dashboard")

    def generate_content(self):
        content = self.panel.content
        content.components = [spc.panel.layout for spc in self.sub_panel_creators.values()]

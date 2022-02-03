import dash_core_components as dcc
import dash_html_components as html

from .MethodResultsPanelCreator import MethodResultsPanelCreator
from .PanelCreator import PanelCreator
from .PerformancePanelCreator import PerformancePanelCreator


class ComparePanelCreator(PanelCreator):
    TITLE = "Compare"
    IS_MAIN_PANEL = True

    def __init__(self, desc_prefix="cmp"):
        super().__init__(desc_prefix)
        self.run1_selector = None
        self.run2_selector = None

        self.add_sub_panel_creator(MethodResultsPanelCreator("m-res-run1", "Method Results - Run 1"))
        self.add_sub_panel_creator(MethodResultsPanelCreator("m-res-run2", "Method Results - Run 2"))
        self.add_sub_panel_creator(PerformancePanelCreator("perf-run1", "Performance - Run 2"))
        self.add_sub_panel_creator(PerformancePanelCreator("perf-run2", "Performance - Run 2"))

    def generate_menu(self):
        cmp_menu = self.panel.get_menu()
        cmp_menu.add_menu_item("select-run", "Select Run").set_dropdown()

    def generate_content(self):
        content = self.panel.content

        for spc in self.sub_panel_creators.values():
            spc.generate_content()
        content.components = [spc.panel.layout for spc in self.sub_panel_creators.values()]

        # TODO - get runs from view interface(?)
        self.run1_selector = dcc.RadioItems(id="run1_selector",
                                            options=[
                                                {"label": "run placeholder1", "value": "run1"},
                                                {"label": "run placeholder2", "value": "run2"},
                                                {"label": "run placeholder3", "value": "run3"}
                                            ])
        self.run2_selector = dcc.RadioItems(id="run2_selector",
                                            options=[
                                                {"label": "run placeholder1", "value": "run1"},
                                                {"label": "run placeholder2", "value": "run2"},
                                                {"label": "run placeholder3", "value": "run3"}
                                            ])

        run_select_list_content = self.panel.get_menu()["select-run"].dropdown.set_content()
        run_select_list_content.components = [
            html.Div(["Run 1:", self.run1_selector]),
            html.Div(["Run 2:", self.run2_selector])]

    # TODO - callback
    def update_run_select_list(self, btn):
        pass


    # TODO - callback
    def update_run1_method_results_panel(self, val, protocols):
        pass


    # TODO - callback
    def update_run1_performance_results_panel(self, val, ae_val, pca_val):
        pass


    # TODO - callback
    def update_run2_method_results_panel(self, val, protocols):
        pass


    # TODO - callback
    def update_run2_performance_results_panel(self, val, ae_val, pca_val):
        pass


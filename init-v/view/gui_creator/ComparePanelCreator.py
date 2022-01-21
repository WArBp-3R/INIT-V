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
        self.run1_method_result_panel_creator = MethodResultsPanelCreator("m-res-run1")
        self.run2_method_result_panel_creator = MethodResultsPanelCreator("m-res-run2")
        self.run1_performance_panel_creator = PerformancePanelCreator("perf-run1")
        self.run2_performance_panel_creator = PerformancePanelCreator("perf-run2")

    def generate_menu(self):
        cmp_menu = self.panel.get_menu()
        cmp_menu.add_menu_item("select-run", "Select Run").set_dropdown()

    def generate_content(self):
        content = self.panel.content

        sub_panel_creators = [
            self.run1_method_result_panel_creator,
            self.run2_method_result_panel_creator,
            self.run1_performance_panel_creator,
            self.run2_performance_panel_creator,
        ]
        for spc in sub_panel_creators:
            spc.generate_content()
        content.components = [spc.panel.layout for spc in sub_panel_creators]

        # TODO - get runs from view interface
        # self.run1_selector = None
        # self.run2_selector = None

        run_select_list_content = self.panel.get_menu()["select-run"].dropdown.set_content()
        run_select_list_content.components = [
            html.Div(["Run 1:", self.run1_selector]),
            html.Div(["Run 2:", self.run2_selector])]

    # callback
    def update_run_select_list(self, btn):
        pass
        # TODO

    # callback
    def update_run1_method_results_panel(self, val, protocols):
        pass
        # TODO

    # callback
    def update_run1_performance_results_panel(self, val, ae_val, pca_val):
        pass
        # TODO

    # callback
    def update_run2_method_results_panel(self, val, protocols):
        pass
        # TODO

    # callback
    def update_run2_performance_results_panel(self, val, ae_val, pca_val):
        pass
        # TODO

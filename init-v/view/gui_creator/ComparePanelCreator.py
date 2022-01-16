import dash_core_components as dcc

from .MethodResultsPanelCreator import MethodResultsPanelCreator
from .PanelCreator import PanelCreator
from .PerformancePanelCreator import PerformancePanelCreator


class DashboardPanelCreator(PanelCreator):
    TITLE = "Compare"
    IS_MAIN_PANEL = True

    def __init__(self, desc_prefix="cmp"):
        super().__init__(desc_prefix)
        self.run1_selector = None
        self.run2_selector = None
        self.run1_method_result_panel_creator = MethodResultsPanelCreator("m-res-run1")
        self.run2_method_result_panel_creator = MethodResultsPanelCreator("m-res-run2")
        self.run_1_performance_panel_creator = PerformancePanelCreator("perf-run1")
        self.run_2_performance_panel_creator = PerformancePanelCreator("perf-run2")

    def generate_menu(self):
        cmp_menu = self.panel.get_menu()
        cmp_menu.add_menu_item("select-run", "Select Run").set_dropdown()

    def generate_content(self):
        pass
        # TODO

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

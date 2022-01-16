import dash_core_components as dcc

from .MethodResultsPanelCreator import MethodResultsPanelCreator
from .PanelCreator import PanelCreator
from .PerformancePanelCreator import PerformancePanelCreator


class DashboardPanelCreator(PanelCreator):
    TITLE = "Compare"
    IS_MAIN_PANEL = True

    def __init__(self, desc_prefix="cmp"):
        super().__init__(desc_prefix)
        self.run1_selector: dcc.RadioItems
        self.run2_selector: dcc.RadioItems
        self.run1_method_result_panel_creator: MethodResultsPanelCreator
        self.run2_method_result_panel_creator: MethodResultsPanelCreator
        self.run_1_performance_panel_creator: PerformancePanelCreator
        self.run_2_performance_panel_creator: PerformancePanelCreator

    def generate_menu(self):
        pass
        # TODO

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

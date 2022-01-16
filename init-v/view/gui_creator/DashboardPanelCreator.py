from typing import Union

from dash.dependencies import Input, State

from .AboutPanelCreator import AboutPanelCreator
from .ConfigPanelCreator import ConfigPanelCreator
from .LaunchPanelCreator import LaunchPanelCreator
from .MethodResultsPanelCreator import MethodResultsPanelCreator
from .NetworkPanelCreator import NetworkPanelCreator
from .PanelCreator import PanelCreator
from .PerformancePanelCreator import PerformancePanelCreator
from .StatisticsPanelCreator import StatisticsPanelCreator


class DashboardPanelCreator(PanelCreator):
    TITLE = "Title Placeholder"
    IS_MAIN_PANEL = True

    def __init__(self, desc_prefix="dashboard"):
        super().__init__(desc_prefix)
        self.config_panel_creator: ConfigPanelCreator
        self.network_panel_creator: NetworkPanelCreator
        self.statistics_panel_creator: StatisticsPanelCreator
        self.method_result_panel_creator: MethodResultsPanelCreator
        self.performance_panel_creator: PerformancePanelCreator
        self.launch_panel_creator: LaunchPanelCreator
        self.about_panel_creator: AboutPanelCreator
        self.run_input_config_states: list[Union[Input, State]]

    def generate_menu(self):
        pass
        # TODO

    def generate_content(self):
        pass
        # TODO

    # callback
    def toggle_about_overlay(self, opn, cls):
        pass
        # TODO

    # callback
    def toggle_launch_overlay(self, cls):
        pass
        # TODO

    # callback
    def update_network_panel(self, protocols, run):
        pass
        # TODO

    # callback
    def update_statistics_panel(self, run, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        pass
        # TODO

    # callback
    def update_method_results_panel(self, protocols, run, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        pass
        # TODO

    # callback
    def update_performance_panel(self, ae_val, pca_val, run, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        pass
        # TODO

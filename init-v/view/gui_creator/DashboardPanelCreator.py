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
        self.config_panel_creator = ConfigPanelCreator()
        self.network_panel_creator = NetworkPanelCreator()
        self.statistics_panel_creator = StatisticsPanelCreator()
        self.method_result_panel_creator = MethodResultsPanelCreator()
        self.performance_panel_creator = PerformancePanelCreator()
        self.launch_panel_creator = LaunchPanelCreator()
        self.about_panel_creator = AboutPanelCreator()
        self.run_input_config_states = None

    def generate_menu(self):
        dashboard_menu = self.panel.get_menu()
        dashboard_menu.add_menu_item("run", "Run")
        dashboard_menu.add_menu_item("compare", "Compare Runs", "/compare")

        files_dd_menu = dashboard_menu.add_menu_item("files", "Files").set_dropdown().set_menu()
        files_dd_menu.add_menu_item("open", "Open")
        files_dd_menu.add_menu_item("save", "Save")
        files_dd_menu.add_menu_item("save-as", "Save As...")
        files_dd_menu.add_menu_item("export-as", "Export As...")

        settings_dd_menu = dashboard_menu.add_menu_item("settings", "Settings").set_dropdown().set_menu()
        settings_dd_menu.add_menu_item("default-config", "Default Config")
        settings_dd_menu.add_menu_item("save-config", "Save Config")
        settings_dd_menu.add_menu_item("export-config", "Export Config")

        help_dd_menu = dashboard_menu.add_menu_item("help", "Help").set_dropdown().set_menu()
        help_dd_menu.add_menu_item("about", "About")

    def generate_content(self):
        content = self.panel.content
        sub_panel_creators = [
            self.config_panel_creator,
            self.network_panel_creator,
            self.statistics_panel_creator,
            self.method_result_panel_creator,
            self.performance_panel_creator,
            self.launch_panel_creator,
            self.about_panel_creator
        ]
        for spc in sub_panel_creators:
            spc.generate_content()
        content.components = [spc.panel.layout for spc in sub_panel_creators]

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

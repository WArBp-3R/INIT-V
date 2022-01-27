import dash_core_components as dcc
from dash.dependencies import Output, Input, State

from .AboutPanelCreator import AboutPanelCreator
from .ConfigPanelCreator import ConfigPanelCreator
from .LaunchPanelCreator import LaunchPanelCreator
from .MethodResultsPanelCreator import MethodResultsPanelCreator
from .NetworkPanelCreator import NetworkPanelCreator
from .PanelCreator import PanelCreator
from .PerformancePanelCreator import PerformancePanelCreator
from .StatisticsPanelCreator import StatisticsPanelCreator

from ..GUI_Handler import app, get_input_id

class DashboardPanelCreator(PanelCreator):
    TITLE = "Title Placeholder"
    IS_MAIN_PANEL = True

    def __init__(self, desc_prefix="dashboard"):
        super().__init__(desc_prefix)

        self.hidden_trigger = None

        self.add_sub_panel_creator(ConfigPanelCreator())
        self.add_sub_panel_creator(NetworkPanelCreator())
        self.add_sub_panel_creator(StatisticsPanelCreator())
        self.add_sub_panel_creator(MethodResultsPanelCreator())
        self.add_sub_panel_creator(PerformancePanelCreator())
        self.add_sub_panel_creator(LaunchPanelCreator())
        self.add_sub_panel_creator(AboutPanelCreator())

        self.run_input_config_states = [
            Input(self.panel.get_menu()["run"].id, "n_clicks"),
            State("length_scaling", "value"),
            State("value_scaling", "value"),
            State("normalization", "value"),
            State("method", "value"),
            State("hidden_layers", "value"),
            State("nodes_in_hidden_layers", "value"),
            State("loss_function", "value"),
            State("epochs", "value"),
            State("optimizer", "value"),
        ]

        self.generate_callbacks()

    def generate_callbacks(self):
        app.callback(
            Output("hidden_trigger", "value"),
            self.run_input_config_states
        )(self.create_new_run)

        app.callback(
            Output(self.sub_panel_creators["about"].panel.id, "style"),
            Input(self.panel.get_menu()["help"].dropdown.menu["about"].id, "n_clicks"),
            Input(self.sub_panel_creators["about"].panel.get_close_btn().id, "n_clicks"),
        )(self.toggle_about_overlay)

        app.callback(
            Output("topology-graph", "elements"),
            Input("hidden_trigger", "value"),
            Input(self.sub_panel_creators["network"].panel.format_specifier("active_protocols"), "value")
        )(self.update_network_panel)

    def generate_menu(self):
        dashboard_menu = self.panel.get_menu()
        dashboard_menu.add_menu_item("run", "Run")
        dashboard_menu.add_menu_item("compare", "Compare Runs", "/cmp")

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

        self.hidden_trigger = dcc.Input(id='hidden_trigger', type="hidden", value="")

        for spc in self.sub_panel_creators.values():
            spc.generate_content()
        content.components = [self.hidden_trigger] + [spc.panel.layout for spc in self.sub_panel_creators.values()]

    # TODO - callback
    def create_new_run(self, run, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        print("CREATING NEW RUN (STUB)")
        print(lsc)
        print(vsc)
        print(nrm)
        print(mtd)
        print(nhl)
        print(lsf)
        print(epc)
        print(opt)
        return run

    # TODO - callback
    def toggle_about_overlay(self, opn, cls):
        button_id = get_input_id()

        result = {}
        if button_id == self.panel.get_menu()["help"].dropdown.menu["about"].id:
            result = {"display": "flex"}
        elif button_id == self.sub_panel_creators["about"].panel.get_close_btn().id:
            result = {"display": "none"}
        else:
            pass
        return result

    # TODO - callback
    def toggle_launch_overlay(self, cls):
        pass

    # TODO - callback
    def update_network_panel(self, hidden, protocols):
        print("Network panel updating...")
        return [
            {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
            {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'one', 'target': 'two'}}
        ]

    # TODO - callback
    def update_statistics_panel(self, hidden):
        pass

    # TODO - callback
    def update_method_results_panel(self, hidden, protocols):
        pass

    # TODO - callback
    def update_performance_panel(self, hidden, ae_val, pca_val):
        pass

    # TODO - callback
    def update_protocols(self):
        pass

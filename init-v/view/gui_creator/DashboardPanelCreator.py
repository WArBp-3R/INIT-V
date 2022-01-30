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

import plotly.graph_objs as go


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

        self.define_callbacks()

    def define_callbacks(self):
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
            Output(self.sub_panel_creators["launch"].panel.id, "style"),
            Input(self.sub_panel_creators["launch"].panel.get_close_btn().id, "n_clicks"),
        )(self.toggle_launch_overlay)

        app.callback(
            Output("topology-graph", "elements"),
            Input("hidden_trigger", "value"),
            Input(self.sub_panel_creators["network"].panel.format_specifier("active_protocols"), "value")
        )(self.update_network_panel)

        # app.callback(
        #     Output("topology-graph", "elements"),
        #     Input("hidden_trigger", "value"),
        #     Input(self.sub_panel_creators["network"].panel.format_specifier("active_protocols"), "value")
        # )(self.update_statistics_panel)

        # TODO - fix output lists
        app.callback(
            Output(self.sub_panel_creators["m-res"].panel.format_specifier("autoencoder_graph"), "figure"),
            Output(self.sub_panel_creators["m-res"].panel.format_specifier("pca_graph"), "figure"),
            Output(self.sub_panel_creators["m-res"].panel.format_specifier("merged_graph"), "figure"),
            # self.sub_panel_creators["m-res"].graph_outputs,
            Input("hidden_trigger", "value"),
            Input(self.sub_panel_creators["m-res"].panel.format_specifier("active_protocols"), "value")
        )(self.update_method_results_panel)

        app.callback(
            Output(self.sub_panel_creators["perf"].panel.format_specifier("autoencoder_graph"), "figure"),
            Output(self.sub_panel_creators["perf"].panel.format_specifier("pca_graph"), "figure"),
            Output(self.sub_panel_creators["perf"].panel.format_specifier("merged_graph"), "figure"),
            # self.sub_panel_creators["perf"].graph_outputs,
            Input("hidden_trigger", "value"),
            Input(self.sub_panel_creators["perf"].panel.format_specifier("accuracy"), "value"),
            Input(self.sub_panel_creators["perf"].panel.format_specifier("data_loss"), "value")
        )(self.update_performance_panel)

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

        self.hidden_trigger = dcc.Input(id="hidden_trigger", type="hidden", value="")

        for spc in self.sub_panel_creators.values():
            spc.generate_content()
        content.components = [self.hidden_trigger] + [spc.panel.layout for spc in self.sub_panel_creators.values()]

    # ------ CALLBACKS
    # TODO - callback replace stub
    def create_new_run(self, run, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        print("CREATING NEW RUN (STUB)")
        # view adapter stuff
        return run

    def toggle_about_overlay(self, opn, cls):
        button_id = get_input_id()
        print("toggle_about_overlay")
        result = {}
        if button_id == self.panel.get_menu()["help"].dropdown.menu["about"].id:
            result = {"display": "flex"}
        elif button_id == self.sub_panel_creators["about"].panel.get_close_btn().id:
            result = {"display": "none"}
        else:
            pass
        return result

    # TODO - launch panel behaviour still unclear
    def toggle_launch_overlay(self, cls):
        button_id = get_input_id()
        print("toggle_launch_overlay")
        result = {}
        if button_id == self.sub_panel_creators["launch"].panel.get_close_btn().id:
            result = {"display": "none"}
        else:
            pass
        return result

    # TODO - replace stub
    def update_network_panel(self, hidden, protocols):
        print("Network panel updating... (STUB)")
        # view adapter stuff

        print("Network panel updated... (STUB)")
        return [
            {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
            {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'one', 'target': 'two'}}
        ]

    # TODO - replace stub
    def update_statistics_panel(self, hidden):
        print("Statistics panel updating... (STUB)")
        # view adapter stuff
        print("Statistics panel updated... (STUB)")

    # TODO - replace stub
    def update_method_results_panel(self, hidden, protocols):
        print("Method Results panel updating... (STUB)")
        # view adapter stuff
        bruh_graph = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        print("Method Results panel updated... (STUB)")
        return bruh_graph, bruh_graph, bruh_graph

    # TODO - replace stub
    def update_performance_panel(self, hidden, ae_val, pca_val):
        print("Performance panel updating... (STUB)")
        # view adapter stuff
        bruh_graph = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        print("Performance panel updated... (STUB)")
        return bruh_graph, bruh_graph, bruh_graph

    # TODO - callback
    def update_protocols(self):
        pass

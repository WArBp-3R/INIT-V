from datetime import datetime

import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State

import os
import easygui

from .AboutPanelCreator import AboutPanelCreator
from .AutoencoderConfigPanelCreator import AutoencoderConfigPanelCreator
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

    def __init__(self, handler, desc_prefix="dashboard"):
        super().__init__(handler, desc_prefix)

        self.hidden_trigger = dcc.Input(id="hidden_trigger", type="hidden", value="")

        self.add_sub_panel_creator(ConfigPanelCreator(handler))
        self.add_sub_panel_creator(NetworkPanelCreator(handler))
        self.add_sub_panel_creator(StatisticsPanelCreator(handler))
        self.add_sub_panel_creator(MethodResultsPanelCreator(handler))
        self.add_sub_panel_creator(PerformancePanelCreator(handler))
        self.add_sub_panel_creator(LaunchPanelCreator(handler))
        self.add_sub_panel_creator(AboutPanelCreator(handler))

        cfg_spc: ConfigPanelCreator = self.sub_panel_creators["cfg"]
        ae_cfg_spc: AutoencoderConfigPanelCreator = cfg_spc.sub_panel_creators["ae-cfg"]

        self.config_states = [
            State(cfg_spc.length_scaling.id, "value"),
            State(cfg_spc.value_scaling.id, "value"),
            State(cfg_spc.normalization.id, "value"),
            State(cfg_spc.method.id, "value"),
            State(ae_cfg_spc.hidden_layers.id, "value"),
            State(ae_cfg_spc.nodes_in_hidden_layers.id, "value"),
            State(ae_cfg_spc.loss_function.id, "value"),
            State(ae_cfg_spc.epochs.id, "value"),
            State(ae_cfg_spc.optimizer.id, "value"),
        ]

        self.define_callbacks()

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
        settings_dd_menu.add_menu_item("restore-default-config", "Restore Default Config")
        settings_dd_menu.add_menu_item("change-default-config", "Change Default Config")
        settings_dd_menu.add_menu_item("save-config", "Save Config")
        settings_dd_menu.add_menu_item("export-config", "Export Config")

        help_dd_menu = dashboard_menu.add_menu_item("help", "Help").set_dropdown().set_menu()
        help_dd_menu.add_menu_item("about", "About")

    def generate_content(self):
        content = self.panel.content

        for spc in self.sub_panel_creators.values():
            spc.generate_content()
        content.components = [self.hidden_trigger] + [spc.panel.layout for spc in self.sub_panel_creators.values()]

    def define_callbacks(self):
        app.callback(
            Output(self.hidden_trigger.id, "value"),
            Input(self.panel.get_menu()["run"].id, "n_clicks"),
            self.config_states
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
            Output(self.sub_panel_creators["network"].topology_graph.id, "elements"),
            Input(self.hidden_trigger.id, "value"),
            Input(self.sub_panel_creators["network"].active_protocols.id, "value")
        )(self.update_network_panel)

        # app.callback(
        # )(self.update_statistics_panel)

        app.callback(
            self.sub_panel_creators["m-res"].graph_outputs,
            Input(self.hidden_trigger.id, "value"),
            Input(self.sub_panel_creators["m-res"].active_protocols.id, "value")
        )(self.update_method_results_panel)

        app.callback(
            self.sub_panel_creators["perf"].graph_outputs,
            Input(self.hidden_trigger.id, "value"),
            Input(self.sub_panel_creators["perf"].accuracy.id, "value"),
            Input(self.sub_panel_creators["perf"].data_loss.id, "value")
        )(self.update_performance_panel)

        app.callback(
            Output(self.panel.get_menu()["files"].dropdown.menu["open"].id, "n_clicks"),
            Input(self.panel.get_menu()["files"].dropdown.menu["open"].id, "n_clicks")
        )(self.open_files_method)

        app.callback(
            Output(self.panel.get_menu()["files"].dropdown.menu["load-session"].id, "n_clicks"),
            Input(self.panel.get_menu()["files"].dropdown.menu["load-session"].id, "n_clicks")
        )(self.load_session)

        app.callback(
            Output(self.panel.get_menu()["files"].dropdown.menu["save-as"].id, "n_clicks"),
            Input(self.panel.get_menu()["files"].dropdown.menu["save-as"].id, "n_clicks")
        )(self.save_as_method)

        app.callback(
            Output(self.panel.get_menu()["files"].dropdown.menu["save"].id, "n_clicks"),
            Input(self.panel.get_menu()["files"].dropdown.menu["save"].id, "n_clicks")
        )(self.save_method)

        app.callback(
            Output(self.panel.get_menu()["settings"].dropdown.menu["default-config"].id, "n_clicks"),
            Input(self.panel.get_menu()["settings"].dropdown.menu["default-config"].id, "n_clicks")
        )(self.default_config)

        app.callback(
            Output(self.panel.get_menu()["settings"].dropdown.menu["set-default-config"].id, "n_clicks"),
            Input(self.panel.get_menu()["settings"].dropdown.menu["set-default-config"].id, "n_clicks")
        )(self.set_as_default_config)

        app.callback(
            Output(self.panel.get_menu()["settings"].dropdown.menu["load-config"].id, "n_clicks"),
            Input(self.panel.get_menu()["settings"].dropdown.menu["load-config"].id, "n_clicks")
        )(self.load_config)

        app.callback(
            Output(self.panel.get_menu()["settings"].dropdown.menu["save-config"].id, "n_clicks"),
            Input(self.panel.get_menu()["settings"].dropdown.menu["save-config"].id, "n_clicks")
        )(self.save_config)

        app.callback(
            Output(self.panel.get_menu()["settings"].dropdown.menu["export-config"].id, "n_clicks"),
            Input(self.panel.get_menu()["settings"].dropdown.menu["export-config"].id, "n_clicks")
        )(self.export_config)

    def generate_menu(self):
        dashboard_menu = self.panel.get_menu()
        dashboard_menu.add_menu_item("run", "Run")
        dashboard_menu.add_menu_item("compare", "Compare Runs", "/cmp")

        files_dd_menu = dashboard_menu.add_menu_item("files", "Files").set_dropdown().set_menu()
        files_dd_menu.add_menu_item("open", "Open")
        files_dd_menu.add_menu_item("load-session", "load session")
        files_dd_menu.add_menu_item("save", "Save")
        files_dd_menu.add_menu_item("save-as", "Save As...")
        files_dd_menu.add_menu_item("export-as", "Export As...")

        settings_dd_menu = dashboard_menu.add_menu_item("settings", "Settings").set_dropdown().set_menu()
        settings_dd_menu.add_menu_item("default-config", "Default Config")
        settings_dd_menu.add_menu_item("set-default-config", "Set as Default Config")
        settings_dd_menu.add_menu_item("save-config", "Save Config")
        settings_dd_menu.add_menu_item("load-config", "Load Config")
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
    # TODO - callback replace stub (WIP)
    def create_new_run(self, run, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        button_id = get_input_id()
        current_run = ""
        if button_id == self.panel.get_menu()["run"].id:
            print("CREATING NEW RUN...")
            self.handler.interface.create_run(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt)
            # current_run = self.handler.interface.get_run_list()[-1]
        else:
            print("Create new run callback triggered")
        # return current_run
        return -1

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

    # TODO - replace stub (WIP)
    def update_network_panel(self, hidden, protocols):
        button_id = get_input_id()

        elements = []
        topology = self.handler.interface.get_network_topology()
        for d in topology.devices:
            elements.append({"data": {"id": d.mac_address, "label": d.mac_address}})

        if button_id == self.hidden_trigger.id:
            print("Network Panel updating...")
            for c in topology.connections:
                for p in c.protocols:
                    elements.append({"data": {"label": p, "source": c.first_device, "target": c.second_device},
                                     "style": {"label": p}})
        elif button_id == self.sub_panel_creators["network"].active_protocols.id:
            print("Network panel protocols change...")
            for c in topology.connections:
                for p in c.protocols:
                    if p in protocols:
                        elements.append(
                            {"data": {"source": c.first_device, "target": c.second_device}, "style": {"label": p}})
        else:
            print("Network panel callback triggered")
        return elements

    # TODO - replace stub (WIP)
    def update_statistics_panel(self, hidden):
        print("Statistics panel updating... (STUB)")
        # view adapter stuff
        print("Statistics panel updated... (STUB)")

    # TODO - replace stub (WIP)
    def update_method_results_panel(self, hidden, protocols):
        button_id = get_input_id()
        ae_data = []
        pca_data = []
        merged_data = []

        if button_id == self.hidden_trigger.id:
            print("Method Results Panel updating...")
            ae_data, pca_data = self.handler.interface.get_method_results(hidden)
            merged_data = ae_data + pca_data
        elif button_id == self.sub_panel_creators["m-res"].active_protocols.id:
            print("Method Results panel protocols change...")
            ae_data_unfiltered, pca_data_unfiltered = self.handler.interface.get_method_results(hidden)
            for d in ae_data_unfiltered:
                if d[3][-1] in protocols:
                    ae_data.append(d)
            for d in pca_data_unfiltered:
                if d[3][-1] in protocols:
                    pca_data.append(d)
            merged_data = ae_data + pca_data
        else:
            print("Method Results panel callback triggered")

        bruh_graph = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        ae_fig = bruh_graph
        pca_fig = bruh_graph
        merged_fig = bruh_graph

        ae_df = dict()
        ae_df["x"] = [d[0] for d in ae_data]
        ae_df["y"] = [d[1] for d in ae_data]
        # ae_df["hover"] = [d[2] for d in ae_data]

        pca_df = dict()
        pca_df["x"] = [d[0] for d in pca_data]
        pca_df["y"] = [d[1] for d in pca_data]
        # pca_df["hover"] = [d[2] for d in pca_data]

        merged_df = dict()
        merged_df["x"] = [d[0] for d in merged_data]
        merged_df["y"] = [d[1] for d in merged_data]
        # merged_df["hover"] = [d[2] for d in merged_data]

        # ae_fig = px.scatter(ae_df, x="x", y="y", hover_data="hover")
        pca_fig = px.scatter(pca_df, x="x", y="y")
        # merged_fig = px.scatter(merged_df, x="x", y="y", hover_data="hover")

        return ae_fig, pca_fig, merged_fig

    # TODO - replace stub (WIP)
    def update_performance_panel(self, hidden, ae_val, pca_val):
        button_id = get_input_id()
        bruh_graph = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        ae_fig = bruh_graph
        pca_fig = bruh_graph
        merged_fig = bruh_graph
        if button_id == self.hidden_trigger.id:
            print("Performance panel updating...")
            pca_data = self.handler.interface.get_performance(hidden)
            # # merged_data = ae_data + pca_data
            #
            # # ae_df = dict()
            # # ae_df["x"] = [d[0] for d in ae_data]
            # # ae_df["y"] = [d[1] for d in ae_data]
            # # ae_df["hover"] = [d[2] for d in ae_data]
            #
            # pca_df["hover"] = [d[2] for d in pca_data]
            #
            # # merged_df = dict()
            # # merged_df["x"] = [d[0] for d in merged_data]
            # # merged_df["y"] = [d[1] for d in merged_data]
            # # merged_df["hover"] = [d[2] for d in merged_data]
            #
            # # ae_fig = px.scatter(ae_df, x="x", y="y")
            pca_df = dict()
            pca_df["y"] = [3, 1]
            pca_df["x"] = ["Training Data", "Test Data"]
            pca_fig = px.bar(pca_df, x="x", y="y")
            # merged_fig = px.scatter(merged_df, x="x", y="y")
        elif button_id == self.sub_panel_creators["perf"].accuracy.id:
            print("Performance panel accuracy change")
        elif button_id == self.sub_panel_creators["perf"].data_loss.id:
            print("Performance panel data loss change")
        else:
            print("Performance panel callback triggered")
        return ae_fig, pca_fig, merged_fig


    def open_files_method(self, button):

        path = easygui.fileopenbox("please select file", "open", "*", ["*.csv", "*.pcapng", "csv and pcapng"], False)
        if path.endswith(".csv"):
            self.handler.interface.load_config(path)
        elif path.endswith(".pacpng"):
            self.handler.interface.create_new_session(path)
        print(path)
        return button

    def load_session(self, button):
        path = easygui.diropenbox("please select a session (top directory).", "load session", "*")
        if path is None:
            return button
        else:
            self.handler.interface.load_session(path)
        print(path)
        return button

    def save_as_method(self, button):
        file = ""
        now = datetime.now()
        timestampStr = now.strftime("%d-%b-%Y (%H-%M-%S.%f)")
        name = easygui.multenterbox("Please enter a name for the session", "save session",["name"], ["session-" + timestampStr])[0]
        dir = easygui.diropenbox("Select Directory to save", "save", None)
        if name is None:
            name = "session-" + timestampStr
        if file is None:
            pass
        else:
            self.handler.interface.save_session(dir + "\\" + name, None)
        return button

    def save_method(self, button):
        self.handler.interface.save_session(None, None)
        return button


    def default_config(self, button):
        self.handler.interface.default_config()
        return button

    def set_as_default_config(self, button):
        self.handler.interface.set_default_config()
        return button

    def load_config(self, button):
        path = self.handler.interface
        path = easygui.fileopenbox("please select config", "load config", "*", ["*.csv", "only csv"], False)
        self.handler.interface.load_config(path)
        return button

    def save_config(self, button):
        now = datetime.now()
        timestampStr = now.strftime("%d-%b-%Y (%H-%M-%S.%f)")
        name = easygui.multenterbox("Please enter a name for the config", "save session", ["name"],
                                    ["config-" + timestampStr])[0]
        self.handler.interface.save_config(name)
        return button

    def export_config(self, button):
        now = datetime.now()
        timestampStr = now.strftime("%d-%b-%Y (%H-%M-%S.%f)")
        name = easygui.multenterbox("Please enter a name for the config", "save session", ["name"],
                                    ["config-" + timestampStr])[0]
        dir = easygui.diropenbox("Select Directory to save to", "save", None)
        self.handler.interface.save_config(dir + "/" + name)
        return button
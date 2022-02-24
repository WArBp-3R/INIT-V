from datetime import datetime

import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Output, Input, State

import os
import easygui

from .AboutPanelCreator import AboutPanelCreator
from .AutoencoderConfigPanelCreator import AutoencoderConfigPanelCreator
from .ConfigPanelCreator import ConfigPanelCreator
from .MethodResultsPanelCreator import MethodResultsPanelCreator
from .NetworkPanelCreator import NetworkPanelCreator
from .PanelCreator import PanelCreator
from .PerformancePanelCreator import PerformancePanelCreator
from .StatisticsPanelCreator import StatisticsPanelCreator

from ..GUI_Handler import app, get_input_id

import plotly.graph_objs as go

from ..utility import MethodResultContainer


class DashboardPanelCreator(PanelCreator):
    TITLE = "Title Placeholder"
    IS_MAIN_PANEL = True

    def __init__(self, handler, desc_prefix="dashboard"):
        super().__init__(handler, desc_prefix)

        self.session_id = dcc.Input(id="session_id", type="hidden", value="")
        self.run_id = dcc.Input(id="run_id", type="hidden", value="")

        self.add_sub_panel_creator(ConfigPanelCreator(handler))
        self.add_sub_panel_creator(NetworkPanelCreator(handler))
        self.add_sub_panel_creator(StatisticsPanelCreator(handler))
        self.add_sub_panel_creator(MethodResultsPanelCreator(handler))
        self.add_sub_panel_creator(PerformancePanelCreator(handler))
        self.add_sub_panel_creator(AboutPanelCreator(handler))

        self.define_callbacks()

    def generate_menu(self):
        dashboard_menu = self.panel.get_menu()
        dashboard_menu.add_menu_item("run", "Run")
        dashboard_menu.add_menu_item("compare", "Compare Runs", "/cmp")

        files_dd_menu = dashboard_menu.add_menu_item("files", "Files").set_dropdown().set_menu()
        files_dd_menu.add_menu_item("open", "Open")
        files_dd_menu.add_menu_item("load-session", "Load Session")
        files_dd_menu.add_menu_item("save", "Save")
        files_dd_menu.add_menu_item("save-as", "Save As...")
        files_dd_menu.add_menu_item("export-as", "Export As...")

        settings_dd_menu = dashboard_menu.add_menu_item("settings", "Settings").set_dropdown().set_menu()
        settings_dd_menu.add_menu_item("set-default-config", "Set Default Config")
        settings_dd_menu.add_menu_item("change-default-config", "Change Default Config")
        settings_dd_menu.add_menu_item("load-config", "Load Config")
        settings_dd_menu.add_menu_item("save-config", "Save Config")
        settings_dd_menu.add_menu_item("export-config", "Export Config")

        help_dd_menu = dashboard_menu.add_menu_item("help", "Help").set_dropdown().set_menu()
        help_dd_menu.add_menu_item("about", "About")

    def generate_content(self):
        content = self.panel.content

        for spc in self.sub_panel_creators.values():
            spc.generate_content()
        content.components = [self.run_id] + [spc.panel.layout for spc in self.sub_panel_creators.values()]

    def define_callbacks(self):
        app.callback(
            Output(self.run_id.id, "value"),
            Input(self.panel.get_menu()["run"].id, "n_clicks"),
        )(self.create_new_run)

        app.callback(
            Output(self.sub_panel_creators["about"].panel.id, "style"),
            Input(self.panel.get_menu()["help"].dropdown.menu["about"].id, "n_clicks"),
            Input(self.sub_panel_creators["about"].panel.get_close_btn().id, "n_clicks"),
        )(self.toggle_about_overlay)

        app.callback(
            Output(self.sub_panel_creators["network"].topology_graph.id, "elements"),
            Input(self.run_id.id, "value"),
            Input(self.sub_panel_creators["network"].active_protocols.id, "value")
        )(self.update_network_panel)

        app.callback(
            self.sub_panel_creators["m-res"].graph_outputs,
            Input(self.run_id.id, "value"),
        )(self.update_method_results_panel)

        app.callback(
            self.sub_panel_creators["perf"].graph_outputs,
            Input(self.run_id.id, "value"),
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
            Output(self.panel.get_menu()["settings"].dropdown.menu["set-default-config"].id, "n_clicks"),
            Input(self.panel.get_menu()["settings"].dropdown.menu["set-default-config"].id, "n_clicks")
        )(self.default_config)

        app.callback(
            Output(self.panel.get_menu()["settings"].dropdown.menu["change-default-config"].id, "n_clicks"),
            Input(self.panel.get_menu()["settings"].dropdown.menu["change-default-config"].id, "n_clicks")
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

    # ------ CALLBACKS
    def create_new_run(self, run):
        button_id = get_input_id()
        if button_id == self.panel.get_menu()["run"].id:
            print("CREATING NEW RUN...")
            self.handler.interface.create_run()
        else:
            print("Create new run callback triggered")
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

    def update_network_panel(self, hidden, protocols):
        button_id = get_input_id()

        elements = []
        topology = self.handler.interface.get_network_topology()
        for d in topology.devices:
            elements.append({"data": {"id": d.mac_address, "label": d.mac_address}})

        if button_id == self.run_id.id:
            print("Network Panel updating...")
            for c in topology.connections:
                elements.append({"data": {"source": c.first_device, "target": c.second_device},
                                 })
        elif button_id == self.sub_panel_creators["network"].active_protocols.id:
            print("Network panel protocols change...")
            for c in topology.connections:
                for p in c.protocols:
                    if p in protocols:
                        elements.append(
                            {"data": {"source": c.first_device, "target": c.second_device}})
        else:
            print("Network panel callback triggered")
        return elements

    def update_method_results_panel(self, hidden, protocols):
        button_id = get_input_id()
        ae_data = []
        pca_data = []

        if button_id == self.hidden_trigger.id:
            print("Method Results Panel updating...")
            ae_data, pca_data = self.handler.interface.get_method_results(hidden)
        elif button_id == self.sub_panel_creators["m-res"].active_protocols.id:
            print("Method Results panel protocols change...")
            ae_data_unfiltered, pca_data_unfiltered = self.handler.interface.get_method_results(hidden)
            for d in ae_data_unfiltered:
                if d[3] in protocols:
                    ae_data.append(d)
            for d in pca_data_unfiltered:
                if d[3] in protocols:
                    pca_data.append(d)
        else:
            print("Method Results panel callback triggered")

        ae_packet_mappings = [(d[0], d[1]) for d in ae_data]
        ae_hover_information = [d[2] for d in ae_data]
        ae_highest_protocols = [d[3] for d in ae_data]

        pca_packet_mappings = [(d[0], d[1]) for d in ae_data]
        pca_hover_information = [d[2] for d in ae_data]
        pca_highest_protocols = [d[3] for d in ae_data]

        ae_container = MethodResultContainer.MethodResultContainer(ae_packet_mappings, ae_highest_protocols,
                                                                   ae_hover_information)
        pca_container = MethodResultContainer.MethodResultContainer(pca_packet_mappings, pca_highest_protocols,
                                                                    pca_hover_information)
        merged_container = MethodResultContainer.merge_result_containers([ae_container, pca_container])

        return ae_container.figure, pca_container.figure, merged_container.figure

    # TODO - replace stub (WIP)
    def update_performance_panel(self, hidden):
        button_id = get_input_id()

        ae_data = []
        pca_data = []

        if button_id == self.run_id.id:
            print("Performance panel updating...")
            ae_data, pca_data = self.handler.interface.get_performance(hidden)
        else:
            print("Performance panel callback triggered")

        ae_df = dict()
        ae_df["epoch"] = []
        ae_df["loss/accuracy"] = []
        ae_df["keys"] = []
        for k in ae_data.history.keys():
            ae_df["epoch"] += ae_data.epoch
            ae_df["loss/accuracy"] += ae_data.history[k]
            ae_df["keys"] += [k for i in range(0, len(ae_data.epoch))]

        pca_df = dict()
        pca_df["y"] = pca_data
        pca_df["x"] = ["Training Data", "Test Data"]

        ae_fig = px.line(ae_df, x="epoch", y="loss/accuracy", color="keys", markers=True)
        pca_fig = px.bar(pca_df, x="x", y="y")

        return ae_fig, pca_fig

    # File Management Callbacks
    def open_files_method(self, button):
        button_id = get_input_id()
        if button_id == self.panel.get_menu()["files"].dropdown.menu["open"].id:
            path = easygui.fileopenbox("please select file", "open", "*", ["*.csv", "*.pcapng", "csv and pcapng"], False)
            if path.endswith(".csv"):
                self.handler.interface.load_config(path)
            elif path.endswith(".pcapng"):
                self.handler.interface.create_new_session(path)
            print(path)
        else:
            pass
        return button

    def load_session(self, button):
        # TODO add topology graph save
        button_id = get_input_id()
        if button_id == self.panel.get_menu()["files"].dropdown.menu["load-session"].id:
            path = easygui.diropenbox("please select a session (top directory).", "load session", "*")
            if path is None:
                return button
            else:
                self.handler.interface.load_session(path)
            print(path)
        else:
            pass
        return button

    def save_as_method(self, button):
        # TODO add topology graph save
        button_id = get_input_id()
        if button_id == self.panel.get_menu()["files"].dropdown.menu["save-as"].id:
            file = ""
            now = datetime.now()
            timestampStr = now.strftime("%d-%b-%Y (%H-%M-%S)")
            name = easygui.multenterbox("Please enter a name for the session", "save session",["name"], ["session-" + timestampStr])[0]
            dir = easygui.diropenbox("Select Directory to save", "save", None)
            if name is None:
                name = "session-" + timestampStr
            if file is None:
                pass
            else:
                self.handler.interface.save_session(dir + os.sep + name, None, None)
        else:
            pass
        return button

    def save_method(self, button):
        # Todo add t_g
        button_id = get_input_id()
        if button_id == self.panel.get_menu()["files"].dropdown.menu["save"].id:
            self.handler.interface.save_session(None, None, None)
        else:
            pass
        return button


    def default_config(self, button):
        button_id = get_input_id()
        if button_id == self.panel.get_menu()["settings"].dropdown.menu["set-default-config"].id:
            self.handler.interface.default_config()
        else:
            pass
        return button

    def set_as_default_config(self, button):
        button_id = get_input_id()
        if button_id == self.panel.get_menu()["settings"].dropdown.menu["change-default-config"].id:
            self.handler.interface.set_default_config()
        else:
            pass
        return button

    def load_config(self, button):
        button_id = get_input_id()
        if button_id == self.panel.get_menu()["settings"].dropdown.menu["load-config"].id:
            path = self.handler.interface
            path = easygui.fileopenbox("please select config", "load config", "*", ["*.csv", "only csv"], False)
            self.handler.interface.load_config(path)
        else:
            pass
        return button

    def save_config(self, button):
        button_id = get_input_id()
        if button_id == self.panel.get_menu()["settings"].dropdown.menu["save-config"].id:
            now = datetime.now()
            timestampStr = now.strftime("%d-%b-%Y (%H-%M-%S)")
            name = easygui.multenterbox("Please enter a name for the config", "save session", ["name"],
                                        ["config-" + timestampStr])[0]
            self.handler.interface.save_config(name + ".csv")
        else:
            pass
        return button

    def export_config(self, button):
        button_id = get_input_id()
        if button_id == self.panel.get_menu()["settings"].dropdown.menu["export-config"].id:
            now = datetime.now()
            timestampStr = now.strftime("%d-%b-%Y (%H-%M-%S)")
            name = easygui.multenterbox("Please enter a name for the config", "save session", ["name"],
                                        ["config-" + timestampStr])[0]
            dir = easygui.diropenbox("Select Directory to save to", "save", None)
            self.handler.interface.save_config(dir + os.sep + name + ".csv")
        else:
            pass
        return button
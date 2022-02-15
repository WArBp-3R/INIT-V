import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Output, Input, State

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
                elements.append({"data": {"source": c.first_device, "target": c.second_device}})
        elif button_id == self.sub_panel_creators["network"].active_protocols.id:
            print("Network panel protocols change...")
            for c in topology.connections:
                boolean = False
                for p in protocols:
                    if p in c.protocols:
                        boolean = True
                        break
                if boolean:
                    elements.append({"data": {"source": c.first_device, "target": c.second_device}})
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
        bruh_graph = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        ae_fig = bruh_graph
        pca_fig = bruh_graph
        merged_fig = bruh_graph
        if button_id == self.hidden_trigger.id:
            print("Method Results Panel updating...")
            ae_data, pca_data = self.handler.interface.get_method_results(hidden)
            merged_data = ae_data + pca_data

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

            ae_fig = px.scatter(ae_df, x="x", y="y")
            pca_fig = px.scatter(pca_df, x="x", y="y")
            merged_fig = px.scatter(merged_df, x="x", y="y")
        elif button_id == self.sub_panel_creators["m-res"].active_protocols.id:
            print("Method Results panel protocols change...")
        else:
            print("Method Results panel callback triggered")
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
            # pca_data = self.handler.interface.get_performance(hidden)
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
            pca_fig = px.bar([3, 5, 5, 1], x="x", y="y")
            # merged_fig = px.scatter(merged_df, x="x", y="y")
        elif button_id == self.sub_panel_creators["perf"].accuracy.id:
            print("Performance panel accuracy change")
        elif button_id == self.sub_panel_creators["perf"].data_loss.id:
            print("Performance panel data loss change")
        else:
            print("Performance panel callback triggered")
        return ae_fig, pca_fig, merged_fig

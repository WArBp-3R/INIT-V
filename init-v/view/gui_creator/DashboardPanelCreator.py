import os
import tkinter.filedialog as fd
from pathlib import Path

import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from flask import request

from .AboutPanelCreator import AboutPanelCreator
from .ClosePanelCreator import ClosePanelCreator
from .ConfigPanelCreator import ConfigPanelCreator
from .LaunchPanelCreator import LaunchPanelCreator
from .NetworkPanelCreator import NetworkPanelCreator
from .PanelCreator import PanelCreator
from .RunResultPanelCreator import RunResultPanelCreator
from .StatisticsPanelCreator import StatisticsPanelCreator


def shutdown(button):
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


class DashboardPanelCreator(PanelCreator):
    TITLE = "INIT-V"
    IS_MAIN_PANEL = True

    def __init__(self, handler, desc_prefix="dashboard"):
        # State value
        self.creating_run = False

        self.confirm_dialog = None
        self.session_id = None

        spc = [x(handler) for x in
               [ConfigPanelCreator, NetworkPanelCreator, StatisticsPanelCreator, RunResultPanelCreator,
                AboutPanelCreator, LaunchPanelCreator, ClosePanelCreator]]

        super().__init__(handler, desc_prefix, sub_panel_creators=spc)

    def generate_menu(self):
        dashboard_menu = self.panel.get_menu()

        files_dd_menu = dashboard_menu.add_menu_item("files", "Files").set_dropdown().set_menu()
        files_dd_menu.add_menu_item("load-pcap", "Load PCAP")
        files_dd_menu.add_menu_item("load-session", "Load Session")
        files_dd_menu.add_menu_item("save", "Save")
        files_dd_menu.add_menu_item("save-as", "Save As...")
        files_dd_menu.add_menu_item("export-as", "Export As... (NOT IMPL)")

        dashboard_menu.add_menu_item("run", "Run")
        dashboard_menu.add_menu_item("compare", "Compare Runs", "/cmp")

        help_dd_menu = dashboard_menu.add_menu_item("help", "Help").set_dropdown().set_menu()
        help_dd_menu.add_menu_item("about", "About")

    def generate_content(self):
        self.confirm_dialog = dcc.ConfirmDialog(
            id=self.panel.format_specifier('confirm-dialog'),
            message='Run Completed',
        )
        self.session_id = dcc.Input(id=self.panel.format_specifier("session_id"), type="hidden", value="")

        self.panel.content.components = [self.session_id, self.confirm_dialog] + [spc.panel.layout for spc in
                                                                                  self.sub_panel_creators.values()]

    def define_callbacks(self):
        super().define_callbacks()

        cfg_spc: ConfigPanelCreator = self.sub_panel_creators["cfg"]
        net_spc: NetworkPanelCreator = self.sub_panel_creators["network"]
        stats_spc: StatisticsPanelCreator = self.sub_panel_creators["stats"]
        run_spc: RunResultPanelCreator = self.sub_panel_creators["run"]
        launch_spc: LaunchPanelCreator = self.sub_panel_creators["launch"]
        close_spc: ClosePanelCreator = self.sub_panel_creators["close"]

        files_dd_menu = self.panel.get_menu()["files"].dropdown.menu
        help_dd_menu = self.panel.get_menu()["help"].dropdown.menu

        """About overlay"""
        self.register_overlay_callback(self.sub_panel_creators["about"],
                                       help_dd_menu["about"])

        """Create Run/Run list"""
        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(run_spc.select_run_list.id, "options"),
             Output(run_spc.select_run_list.id, "value")], {
                Input(self.session_id.id, "value"): (run_spc.update_select_run_list, None),
                Input(self.panel.get_menu()["run"].id, "n_clicks"): (self.create_run, None)
            },
            [[{"label": "No runs - Create new run by clicking 'Run'", "value": ""}], [""]]
        )

        """Error status"""
        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(cfg_spc.run_config_error_status.id, "children"),
             Output(cfg_spc.run_config_error_status.id, "style")], {
                Input(self.panel.get_menu()["run"].id, "n_clicks"): (
                    self.check_run_config_status, None),
                Input(self.confirm_dialog.id, "displayed"): (
                    lambda x, c, s: ["", {"display": "none"}] if not x else [c, s],
                    [State(cfg_spc.run_config_error_status.id, "children"),
                     State(cfg_spc.run_config_error_status.id, "style")]
                )
            },
            ["", {"display": "none"}]
        )

        """Run done config"""
        self.handler.cb_mgr.register_callback(
            [Output(self.confirm_dialog.id, "displayed")],
            Input(run_spc.select_run_list.id, "options"),
            self.confirm_new_run,
            default_outputs=[False]
        )

        """Updating stats list"""
        self.handler.cb_mgr.register_callback(
            [Output(stats_spc.stats_list.id, "options")],
            Input(self.session_id.id, "value"),
            stats_spc.update_stats_list,
            default_outputs=[[]]
        )

        """Opening session/new session through PCAP"""
        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(self.session_id.id, "value")], {
                Input(files_dd_menu["load-session"].id, "n_clicks"): (self.load_session, None),
                Input(files_dd_menu["load-pcap"].id, "n_clicks"): (self.load_pcap, None),
                Input(launch_spc.open_session_button.id, "n_clicks"): (self.load_session, None),
                Input(launch_spc.open_pcap_button.id, "n_clicks"): (self.load_pcap, None),
                Input(launch_spc.open_previous_button.id, "n_clicks"): (self.load_previous, None)
            },
            [""]
        )

        """Close panel"""
        for i, f in zip([close_spc.save_button, close_spc.save_as_button, close_spc.exit_button],
                        [self.save_method, self.save_as_method, shutdown]):
            self.handler.cb_mgr.register_callback(
                self.handler.void_output,
                Input(i.id, "n_clicks"),
                f
            )

        """Launch panel"""
        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(launch_spc.panel.id, "style")], {
                Input(self.session_id.id,
                      "value"): (
                    lambda x: [{"display": "none"}] if self.handler.interface.get_session_path() else [
                        {"display": "flex"}],
                    None)
            },
            [{}]
        )

        """Smart shutdown"""
        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(close_spc.panel.id, "style")], {
                Input(self.panel.get_close_btn().id,
                      "n_clicks"): (self.smart_shutdown, None),
                Input(launch_spc.panel.get_close_btn().id,
                      "n_clicks"): (self.smart_shutdown, None),
                Input(close_spc.panel.get_close_btn().id,
                      "n_clicks"): (lambda x: [{"display": "none"}], None),
                Input(launch_spc.panel.get_close_btn().id,
                      "n_clicks"): (self.smart_shutdown, None)
            },
            [{}]
        )

        """Display session name"""
        self.handler.cb_mgr.register_callback(
            [Output(self.panel.titlebar.title.id, "children")],
            Input(self.session_id.id, "value"),
            lambda x: [f"{self.TITLE} {self.handler.interface.get_pcap_name()}"],
            default_outputs=[self.TITLE]
        )

        """Load active config from session"""
        self.handler.cb_mgr.register_callback(
            cfg_spc.cfg_outputs,
            Input(self.session_id.id, "value"),
            lambda x: list(self.handler.interface.unpack_config(self.handler.interface.get_active_config()))
        )

        """Create protocol list"""
        self.handler.cb_mgr.register_callback(
            [Output(net_spc.active_protocols.id, "options"),
             Output(net_spc.active_protocols.id, "value")],
            Input(self.session_id.id, "value"),
            net_spc.update_protocols,
            [State(net_spc.edge_view_mode.id, "value")],
            default_outputs=[[], []]
        )

        """Create network topology"""
        self.handler.cb_mgr.register_callback(
            net_spc.topology_outputs,
            Input(self.session_id.id, "value"),
            net_spc.create_topology,
            [State(net_spc.edge_view_mode.id, "value"),
             State(net_spc.active_protocols.id, "value")]
        )

        """Load selected statistic graph"""
        self.handler.cb_mgr.register_callback(
            [Output(stats_spc.stat_graph.id, "figure")],
            Input(self.session_id.id, "value"),
            lambda v, s: [self.handler.interface.get_statistics().statistics[s]],
            [State(stats_spc.stats_list.id, "value")]
        )

        """Save session as"""
        self.handler.cb_mgr.register_callback(
            self.handler.void_output,
            Input(files_dd_menu["save-as"].id, "n_clicks"),
            self.save_as_method
        )

        """Save session"""
        self.handler.cb_mgr.register_callback(
            self.handler.void_output,
            Input(files_dd_menu["save"].id, "n_clicks"),
            self.save_method,
        )

    def create_run(self, button):
        if self.handler.interface.is_active_config_valid():
            self.creating_run = True
        self.handler.interface.create_run()
        return self.sub_panel_creators["run"].update_select_run_list(None)

    # CALLBACK METHODS
    def check_run_config_status(self, button):
        status_ok = [f"config ok! Creating run #{len(self.handler.interface.get_run_list())}...",
                     {"display": "block", "background-color": "#60c000"}]
        status_invalid_config = ["Error: invalid config!", {"display": "block", "background-color": "#c00000"}]
        return status_ok if self.handler.interface.is_active_config_valid() else status_invalid_config

    def confirm_new_run(self, void):
        result = self.creating_run
        self.creating_run = False
        return [result]

    def load_session(self, button):
        path = self.handler.atomic_tk(fd.askdirectory,
                                      initialdir=f"{self.handler.interface.get_workspace_path()}{os.sep}Saves",
                                      title="Select session folder.")
        self.handler.interface.load_session(path)
        return [path]

    def load_pcap(self, button):
        path = self.handler.atomic_tk(fd.askopenfilename,
                                      filetypes=[("Packet Capture", ".pcap .pcapng")],
                                      initialdir=Path.home(),
                                      title="Select PCAP file to load.")
        self.handler.interface.create_new_session(path)
        self.handler.app.title = 'INIT-V ' + self.handler.interface.get_pcap_name()
        return [path]

    def load_previous(self, button):
        self.handler.interface.load_session("#prev")
        return [self.handler.interface.get_session_path()]

    def save_as_method(self, button):
        session_path = self.handler.atomic_tk(fd.asksaveasfilename,
                                              filetypes=[("Folder", "")],
                                              initialdir=f"{self.handler.interface.get_workspace_path()}{os.sep}Saves",
                                              title="Save session")
        self.handler.interface.save_session(session_path, None)
        return [button]

    def save_method(self, button):
        self.handler.interface.save_session(None, None)
        return [button]

    def smart_shutdown(self, button) -> list[dict]:
        if self.handler.interface.get_session_path() is None:
            shutdown(None)
        return [{"display": "flex"}]

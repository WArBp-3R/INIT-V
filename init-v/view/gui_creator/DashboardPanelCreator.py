import os
import tkinter.filedialog as fd
from pathlib import Path

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from .AboutPanelCreator import AboutPanelCreator
from .ConfigPanelCreator import ConfigPanelCreator
from .LaunchPanelCreator import LaunchPanelCreator
from .NetworkPanelCreator import NetworkPanelCreator
from .PanelCreator import PanelCreator
from .RunResultPanelCreator import RunResultPanelCreator
from .StatisticsPanelCreator import StatisticsPanelCreator

class DashboardPanelCreator(PanelCreator):
    TITLE = "INIT-V"
    IS_MAIN_PANEL = True

    def __init__(self, handler, desc_prefix="dashboard"):
        self.session_id = None

        spc = [x(handler) for x in
               [ConfigPanelCreator, NetworkPanelCreator, StatisticsPanelCreator, RunResultPanelCreator,
                AboutPanelCreator, LaunchPanelCreator]]

        super().__init__(handler, desc_prefix, sub_panel_creators=spc)

    def generate_menu(self):
        dashboard_menu = self.panel.get_menu()
        dashboard_menu.add_menu_item("run", "Run")
        dashboard_menu.add_menu_item("compare", "Compare Runs", "/cmp")

        files_dd_menu = dashboard_menu.add_menu_item("files", "Files").set_dropdown().set_menu()
        files_dd_menu.add_menu_item("load-pcap", "Load PCAP")
        files_dd_menu.add_menu_item("load-session", "Load Session")
        files_dd_menu.add_menu_item("save", "Save")
        files_dd_menu.add_menu_item("save-as", "Save As...")
        files_dd_menu.add_menu_item("export-as", "Export As... (NOT IMPL)")

        help_dd_menu = dashboard_menu.add_menu_item("help", "Help").set_dropdown().set_menu()
        help_dd_menu.add_menu_item("about", "About")

        # dcc.Alert("This is a danger alert. Scary!", color="danger")

    def generate_content(self):
        self.session_id = dcc.Input(id="session_id", type="hidden", value="")

        self.panel.content.components = [self.session_id] + [spc.panel.layout for spc in
                                                             self.sub_panel_creators.values()]

    def define_callbacks(self):
        super().define_callbacks()

        cfg_spc: ConfigPanelCreator = self.sub_panel_creators["cfg"]
        net_spc: NetworkPanelCreator = self.sub_panel_creators["network"]
        stats_spc: StatisticsPanelCreator = self.sub_panel_creators["stats"]
        run_spc: RunResultPanelCreator = self.sub_panel_creators["run"]
        launch_spc: LaunchPanelCreator = self.sub_panel_creators["launch"]

        files_dd_menu = self.panel.get_menu()["files"].dropdown.menu
        help_dd_menu = self.panel.get_menu()["help"].dropdown.menu

        self.register_overlay_callback(self.sub_panel_creators["about"],
                                       help_dd_menu["about"])

        # returns -1 for the last run to display
        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(run_spc.run_ids.id, "value")], {
                Input(self.session_id.id, "value"): (lambda x: [-1], None),
                Input(self.panel.get_menu()["run"].id, "n_clicks"): (self.create_run, None)
            },
            [""]
        )

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

        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(launch_spc.panel.id, "style")], {
                Input(self.session_id.id,
                      "value"): (
                    lambda x: [{"display": "none"}] if self.handler.interface.get_session_path() else [
                        {"display": "flex"}],
                    None),
                Input(launch_spc.panel.get_close_btn().id,
                      "n_clicks"): (lambda x: [{"display": "none"}], None)
            },
            [{}]
        )

        self.handler.cb_mgr.register_callback(
            [Output(self.panel.titlebar.title.id, "children")],
            Input(self.session_id.id, "value"),
            lambda x: [f"{self.TITLE} {self.handler.interface.get_pcap_name()}"],
            default_outputs=[self.TITLE]
        )

        self.handler.cb_mgr.register_callback(
            cfg_spc.cfg_outputs,
            Input(self.session_id.id, "value"),
            lambda x: list(self.handler.interface.unpack_config(self.handler.interface.get_active_config()))
        )

        self.handler.cb_mgr.register_callback(
            net_spc.topology_outputs,
            Input(self.session_id.id, "value"),
            net_spc.create_topology,
        )

        self.handler.cb_mgr.register_callback(
            [Output(stats_spc.stat_graph.id, "figure")],
            Input(self.session_id.id, "value"),
            lambda v, s: [self.handler.interface.get_statistics().statistics[s]],
            [State(stats_spc.stats_list.id, "value")]
        )

        self.handler.cb_mgr.register_callback(
            [Output(files_dd_menu["save-as"].id, "n_clicks")],
            Input(files_dd_menu["save-as"].id, "n_clicks"),
            self.save_as_method
        )

        self.handler.cb_mgr.register_callback(
            [Output(files_dd_menu["save"].id, "n_clicks")],
            Input(files_dd_menu["save"].id, "n_clicks"),
            self.save_method,
        )

    # helper method
    def illegal_config(self):
        # will trigger if config was illegal for the run.
        print("bruh wtf bro")
        return -1

    # CALLBACK METHODS
    def create_run(self, button):
        return [self.illegal_config if self.handler.interface.create_run() == 0 else -1]

    def load_session(self, button):
        path = self.handler.atomic_tk(fd.askdirectory,
                                      initialdir=os.path.abspath("../../out/Saves/"),
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
                                              initialdir=os.path.abspath("../../out/Saves/"),
                                              title="Save session")
        self.handler.interface.save_session(session_path, None)
        return [button]

    def save_method(self, button):
        self.handler.interface.save_session(None, None)
        return [button]

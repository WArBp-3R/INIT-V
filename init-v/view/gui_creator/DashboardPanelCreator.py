import os
from datetime import datetime

import dash_core_components as dcc
import easygui
from dash.dependencies import Output, Input

from .AboutPanelCreator import AboutPanelCreator
from .ConfigPanelCreator import ConfigPanelCreator
from .MethodResultsPanelCreator import MethodResultsPanelCreator
from .NetworkPanelCreator import NetworkPanelCreator
from .PanelCreator import PanelCreator
from .PerformancePanelCreator import PerformancePanelCreator
from .StatisticsPanelCreator import StatisticsPanelCreator
from ..GUI_Handler import get_input_id


class DashboardPanelCreator(PanelCreator):
    TITLE = "Title Placeholder"
    IS_MAIN_PANEL = True

    def __init__(self, handler, desc_prefix="dashboard"):
        super().__init__(handler, desc_prefix)

        self.session_id = dcc.Input(id="session_id", type="hidden")
        self.run_id = dcc.Input(id="run_id", type="hidden")

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

        help_dd_menu = dashboard_menu.add_menu_item("help", "Help").set_dropdown().set_menu()
        help_dd_menu.add_menu_item("about", "About")

    def generate_content(self):
        content = self.panel.content

        for spc in self.sub_panel_creators.values():
            spc.generate_content()
        content.components = [self.run_id] + [spc.panel.layout for spc in self.sub_panel_creators.values()]

    def define_callbacks(self):
        net_spc: NetworkPanelCreator = self.sub_panel_creators["network"]
        m_res_spc: MethodResultsPanelCreator = self.sub_panel_creators["m-res"]
        perf_spc: PerformancePanelCreator = self.sub_panel_creators["perf"]

        files_dd_menu = self.panel.get_menu()["files"].dropdown.menu
        help_dd_menu = self.panel.get_menu()["help"].dropdown.menu

        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(self.run_id.id, "value")], {
                Input(self.panel.get_menu()["run"].id,
                      "n_clicks"): (lambda x: [self.handler.interface.create_run()], None)
            },
        )

        self.register_overlay_callback(self.sub_panel_creators["about"],
                                       help_dd_menu["about"])

        self.handler.cb_mgr.register_callback(
            [Output(net_spc.topology_graph.id, "elements")],
            Input(self.run_id.id, "value"),
            net_spc.create_topology,
            default_outputs=[{}]
        )

        self.handler.cb_mgr.register_callback(
            m_res_spc.graph_outputs,
            Input(self.run_id.id, "value"),
            m_res_spc.update_method_results_panel,
            default_outputs=[None, None, None]
        )

        self.handler.cb_mgr.register_callback(
            perf_spc.graph_outputs,
            Input(self.run_id.id, "value"),
            perf_spc.update_performance_panel,
            default_outputs=[None, None]
        )

        # self.handler.app.callback(
        #     Output(files_dd_menu["open"].id, "n_clicks"),
        #     Input(files_dd_menu["open"].id, "n_clicks")
        # )(self.open_files_method)
        #
        # self.handler.app.callback(
        #     Output(files_dd_menu["load-session"].id, "n_clicks"),
        #     Input(files_dd_menu["load-session"].id, "n_clicks")
        # )(self.load_session)
        #
        # self.handler.app.callback(
        #     Output(files_dd_menu["save-as"].id, "n_clicks"),
        #     Input(files_dd_menu["save-as"].id, "n_clicks")
        # )(self.save_as_method)
        #
        # self.handler.app.callback(
        #     Output(files_dd_menu["save"].id, "n_clicks"),
        #     Input(files_dd_menu["save"].id, "n_clicks")
        # )(self.save_method)

    # CALLBACK METHODS
    # def open_files_method(self, button):
    #     button_id = get_input_id()
    #     if button_id == files_dd_menu["open"].id:
    #         path = easygui.fileopenbox("please select file", "open", "*", ["*.csv", "*.pcapng", "csv and pcapng"],
    #                                    False)
    #         if path.endswith(".csv"):
    #             self.handler.interface.load_config(path)
    #         elif path.endswith(".pcapng"):
    #             self.handler.interface.create_new_session(path)
    #         print(path)
    #     else:
    #         pass
    #     return button
    #
    # def load_session(self, button):
    #     # TODO add topology graph save
    #     button_id = get_input_id()
    #     if button_id == files_dd_menu["load-session"].id:
    #         path = easygui.diropenbox("please select a session (top directory).", "load session", "*")
    #         if path is None:
    #             return button
    #         else:
    #             self.handler.interface.load_session(path)
    #         print(path)
    #     else:
    #         pass
    #     return button
    #
    # def save_as_method(self, button):
    #     # TODO add topology graph save
    #     button_id = get_input_id()
    #     if button_id == files_dd_menu["save-as"].id:
    #         file = ""
    #         now = datetime.now()
    #         timestampStr = now.strftime("%d-%b-%Y (%H-%M-%S)")
    #         name = easygui.multenterbox("Please enter a name for the session", "save session", ["name"],
    #                                     ["session-" + timestampStr])[0]
    #         dir = easygui.diropenbox("Select Directory to save", "save", None)
    #         if name is None:
    #             name = "session-" + timestampStr
    #         if file is None:
    #             pass
    #         else:
    #             self.handler.interface.save_session(dir + os.sep + name, None, None)
    #     else:
    #         pass
    #     return button
    #
    # def save_method(self, button):
    #     # Todo add t_g
    #     button_id = get_input_id()
    #     if button_id == files_dd_menu["save"].id:
    #         self.handler.interface.save_session(None, None, None)
    #     else:
    #         pass
    #     return button

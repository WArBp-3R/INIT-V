import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import logging

import tkinter as tk

from view.ViewInterface import ViewInterface


class GUIHandler:
    def __init__(self, interface: ViewInterface):
        self.interface = interface

        self.app = dash.Dash(__name__, suppress_callback_exceptions=True)
        self.app.title = 'INIT-V'

        from view.callback_manager.CallbackManager import CallbackManager
        self.cb_mgr = CallbackManager(self)

        self.void = dcc.Input(id="void", type="hidden", value="")
        self.void_output = [Output(self.void.id, "value")]

        self.url = dcc.Location(id="url")
        self.window = html.Div(id="window")

        # import main panel creators
        from .gui_creator.ComparePanelCreator import ComparePanelCreator
        from .gui_creator.DashboardPanelCreator import DashboardPanelCreator
        from view.gui_creator.PanelCreator import PanelCreator
        dashboard_panel_creator = DashboardPanelCreator(self)
        compare_panel_creator = ComparePanelCreator(self)

        self.panel_creators = {}
        self.generate_panel_creators([dashboard_panel_creator, compare_panel_creator])
        self.default_panel_creator: PanelCreator = self.panel_creators[dashboard_panel_creator.panel.desc_prefix]

        self.app.layout = self.get_layout()

        self.cb_mgr.register_callback(
            [Output(self.window.id, "children")],
            Input(self.url.id, "pathname"),
            self.display_page,
            default_outputs=[self.default_panel_creator.panel.layout]
        )

        self.cb_mgr.finalize_callbacks()
        logging.debug('GUI handler intialized')

    def generate_panel_creators(self, panel_creators):
        from view.gui_creator.PanelCreator import PanelCreator
        sub_panel_creators: dict[str, PanelCreator] = {}
        for pc in panel_creators:
            sub_panel_creators[pc.panel.desc_prefix] = pc
        for spc in sub_panel_creators.values():
            self.generate_panel_creators(spc.sub_panel_creators.values())
        self.panel_creators.update(sub_panel_creators)

    def get_layout(self):
        return html.Div(id="app", children=[self.void, self.url, self.window])

    def display_page(self, path):  # callback
        path_str = str(path)[1:]
        if path_str in self.panel_creators:
            return [self.panel_creators[path_str].panel.layout]
        else:
            return [self.default_panel_creator.panel.layout]

    def run_app(self):
        logging.debug("--------------------------------\n| DASH APP NOW RUNNING...\n--------------------------------")
        self.app.run_server(debug=False)

    def atomic_tk(self, func, **kwargs):
        root = tk.Tk()
        root.wm_attributes('-topmost', 1)
        root.withdraw()
        result = func(**kwargs)
        root.destroy()
        return result

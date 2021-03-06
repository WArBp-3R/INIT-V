from ..GUI_Handler import GUIHandler
from ..gui_component.Panel import Panel

from dash.dependencies import Output, Input

import logging
from flask import request

class PanelCreator:
    TITLE = ""
    IS_OVERLAY = False
    IS_MAIN_PANEL = False

    def __init__(self, handler: GUIHandler, desc_prefix: str, title=None, sub_panel_creators=None):
        self.handler = handler

        if not title:
            title = self.TITLE
        self.panel = Panel(desc_prefix, title, is_overlay=self.IS_OVERLAY, is_main_panel=self.IS_MAIN_PANEL)
        self.sub_panel_creators = {}
        if sub_panel_creators:
            for spc in sub_panel_creators:
                self.add_sub_panel_creator(spc)

        self.generate_menu()
        self.generate_content()
        self.define_callbacks()

    def add_sub_panel_creator(self, sub_panel_creator):
        self.sub_panel_creators[sub_panel_creator.panel.desc_prefix] = sub_panel_creator

    def generate_menu(self):
        pass

    def generate_content(self):
        pass

    def define_callbacks(self):
        if self.panel.titlebar.min_btn:
            self.handler.cb_mgr.register_callback(
                [Output(self.panel.content.id, "style")],
                Input(self.panel.get_min_btn().id, "n_clicks"),
                lambda x: [{"display": "none"}] if x % 2 == 1 else [{"display": "flex"}],
                default_outputs=[{}]
            )

    def register_overlay_callback(self, overlay_pc, open_button):
        overlay_panel = overlay_pc.panel
        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(overlay_panel.id, "style")], {
                Input(open_button.id, "n_clicks"): (lambda x: [{"display": "flex"}], None),
                Input(overlay_panel.get_close_btn().id, "n_clicks"): (lambda x: [{"display": "none"}], None),
            },
            [{}]
        )
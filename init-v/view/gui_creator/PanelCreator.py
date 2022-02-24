from ..GUI_Handler import GUIHandler
from ..gui_component.Panel import Panel

from dash.dependencies import Output, Input

from ..GUI_Handler import app, get_input_id


class PanelCreator:
    TITLE = ""
    IS_OVERLAY = False
    IS_MAIN_PANEL = False

    def __init__(self, handler: GUIHandler, desc_prefix: str, title=None, sub_panel_creators=None):
        if title is None:
            title = self.TITLE
        if sub_panel_creators is None:
            self.sub_panel_creators = {}
        self.handler = handler
        self.panel = Panel(desc_prefix, title, is_overlay=self.IS_OVERLAY, is_main_panel=self.IS_MAIN_PANEL)
        self.generate_menu()

    def add_sub_panel_creator(self, sub_panel_creator):
        self.sub_panel_creators[sub_panel_creator.panel.desc_prefix] = sub_panel_creator

    def generate_menu(self):
        pass

    def generate_content(self):
        pass

    def define_callbacks(self):
        if self.panel.titlebar.min_btn:
            app.callback(
                Output(self.panel.content.id, "style"),
                Input(self.panel.get_min_btn().id, "n_clicks"),
            )(self.minimize_panel)

    # CALLBACKS
    def minimize_panel(self, btn):
        print("minimize_panel")

        button_id = get_input_id()
        result = {}
        if button_id == self.panel.get_min_btn().id:
            if btn % 2 == 1:
                result = {"display": "none"}
            else:
                result = {"display": "inherit"}
        else:
            pass
        return result

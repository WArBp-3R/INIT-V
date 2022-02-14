from ..GUI_Handler import GUIHandler
from ..gui_component.Panel import Panel


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
        pass

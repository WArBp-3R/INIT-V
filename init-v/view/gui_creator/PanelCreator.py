from ..gui_component.Panel import Panel


class PanelCreator:
    TITLE = ""
    IS_OVERLAY = False
    IS_MAIN_PANEL = False

    def __init__(self, desc_prefix):
        self.panel = Panel(desc_prefix, title=self.TITLE, is_overlay=self.IS_OVERLAY, is_main_panel=self.IS_MAIN_PANEL)
        self.generate_menu()

    def generate_menu(self):
        pass

    def generate_content(self):
        pass

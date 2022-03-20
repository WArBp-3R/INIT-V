from .PanelCreator import PanelCreator
from ..gui_component.InteractElement import InteractElement


class ClosePanelCreator(PanelCreator):
    TITLE = "CLOSE"
    IS_OVERLAY = True

    def __init__(self, handler, desc_prefix="close"):
        self.save_button = None
        self.save_as_button = None
        self.exit_button = None
        super().__init__(handler, desc_prefix)

    def generate_menu(self):
        launch_menu = self.panel.get_menu()
        self.save_button = launch_menu.add_menu_item("save", "Save session")
        self.save_as_button = launch_menu.add_menu_item("save_as", "Save session as")
        self.exit_button = launch_menu.add_menu_item("exit", "Exit")

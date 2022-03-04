from .PanelCreator import PanelCreator
from ..gui_component.InteractElement import InteractElement


class LaunchPanelCreator(PanelCreator):
    TITLE = "Launch"
    IS_OVERLAY = True

    def __init__(self, handler, desc_prefix="launch"):
        self.open_pcap_button = None
        self.open_previous_button = None
        self.open_session_button = None
        super().__init__(handler, desc_prefix)

    def generate_menu(self):
        launch_menu = self.panel.get_menu()
        self.open_pcap_button = launch_menu.add_menu_item("open-pcap", "Open PCAP")
        self.open_previous_button = launch_menu.add_menu_item("open-previous", "Open Previous Session")
        self.open_session_button = launch_menu.add_menu_item("open-session", "Open Session")

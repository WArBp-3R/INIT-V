from .PanelCreator import PanelCreator
from ..gui_component.InteractElement import InteractElement


class LaunchPanelCreator(PanelCreator):
    TITLE = "Launch"
    IS_OVERLAY = True

    def __init__(self, desc_prefix="launch"):
        super().__init__(desc_prefix)
        self.open_pcap_button = None
        self.open_previous = None
        self.session = None

    def generate_menu(self):
        pass

    # TODO
    def generate_content(self):
        content = self.panel.content

from .PanelCreator import PanelCreator
from ..gui_component.InteractElement import InteractElement


class LaunchPanelCreator(PanelCreator):
    TITLE = "Launch"
    IS_OVERLAY = True

    def __init__(self, desc_prefix="launch"):
        super().__init__(desc_prefix)
        self.open_pcap_button = None
        self.open_previous = None
        self.open_session = None

    def generate_menu(self):
        pass

    def generate_content(self):
        content = self.panel.content

        self.open_pcap_button = InteractElement(self.panel.format_specifier("open-pcap"), "Open PCAP")
        self.open_previous = InteractElement(self.panel.format_specifier("open-previous"), "Open Previous")
        self.open_session = InteractElement(self.panel.format_specifier("open-session"), "Open Session")

        content.components = [self.open_pcap_button, self.open_previous, self.open_session]

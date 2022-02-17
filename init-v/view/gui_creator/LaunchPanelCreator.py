from .PanelCreator import PanelCreator
from ..gui_component.InteractElement import InteractElement


class LaunchPanelCreator(PanelCreator):
    TITLE = "Launch"
    IS_OVERLAY = True

    def __init__(self, handler, desc_prefix="launch"):
        super().__init__(handler, desc_prefix)
        self.open_pcap_button = InteractElement(self.panel.format_specifier("open-pcap"), "Open PCAP")
        self.open_previous = InteractElement(self.panel.format_specifier("open-previous"), "Open Previous")
        self.open_session = InteractElement(self.panel.format_specifier("open-session"), "Open Session")

    def generate_menu(self):
        pass

    def generate_content(self):
        content = self.panel.content

        content.components = [ie.layout for ie in [self.open_pcap_button, self.open_previous, self.open_session]]

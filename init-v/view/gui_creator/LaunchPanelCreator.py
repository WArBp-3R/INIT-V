from .PanelCreator import PanelCreator
from ..gui_component.InteractElement import InteractElement


class LaunchPanelCreator(PanelCreator):
    TITLE = "Launch"
    IS_OVERLAY = True

    def __init__(self, desc_prefix="launch"):
        super().__init__(desc_prefix)
        self.open_pcap_button: InteractElement
        self.open_previous: InteractElement
        self.session: InteractElement

    def generate_menu(self):
        pass

    def generate_content(self):
        pass
        # TODO

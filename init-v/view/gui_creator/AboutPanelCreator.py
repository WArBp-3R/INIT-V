import dash_html_components as html

from .PanelCreator import PanelCreator


class AboutPanelCreator(PanelCreator):
    TITLE = "About"
    IS_OVERLAY = True

    def __init__(self, handler, desc_prefix="about"):
        self.logo = None
        self.version = None
        super().__init__(handler, desc_prefix)

    def generate_menu(self):
        pass

    def generate_content(self):
        # TODO - define content
        self.panel.content.components = []

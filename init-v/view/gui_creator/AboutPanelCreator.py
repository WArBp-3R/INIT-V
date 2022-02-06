import dash_html_components as html

from .PanelCreator import PanelCreator


class AboutPanelCreator(PanelCreator):
    TITLE = "About"
    IS_OVERLAY = True

    def __init__(self, handler, desc_prefix="about"):
        super().__init__(handler, desc_prefix)
        self.logo = None
        self.version = None

    def generate_menu(self):
        pass

    def generate_content(self):
        content = self.panel.content

        # TODO - define content
        content.components = []

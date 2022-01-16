import dash_html_components as html

from .PanelCreator import PanelCreator


class AboutPanelCreator(PanelCreator):
    TITLE = "About"
    IS_OVERLAY = True

    def __init__(self, desc_prefix="about"):
        super().__init__(desc_prefix)
        self.logo: html.Img
        self.version: html.Span

    def generate_menu(self):
        pass
        # TODO

    def generate_content(self):
        pass
        # TODO

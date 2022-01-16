import dash_html_components as html

from .PanelCreator import PanelCreator


class AboutPanelCreator(PanelCreator):
    TITLE = "About"
    IS_OVERLAY = True

    def __init__(self, desc_prefix="about"):
        super().__init__(desc_prefix)
        self.logo = None
        self.version = None

    def generate_menu(self):
        pass

    def generate_content(self):
        pass
        # TODO

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
        self.panel.content.components = [html.P('This program was created in an educational context by computer science'
                                                'students at the KIT (namely Deniz İmge Avcı, Johannes Heid, Mark Hempe'
                                                'l, Thorben Comes and Walter Alexander Böttcher). Therefore it will not'
                                                ' be supported after its first release. For questions about the backend'
                                                ' try to contact the Fraunhofer in Karlsruhe.')]

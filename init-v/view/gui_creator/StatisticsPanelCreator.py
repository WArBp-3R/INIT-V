from .PanelCreator import PanelCreator


class StatisticsPanelCreator(PanelCreator):
    TITLE = "Statistics"

    def __init__(self, handler, desc_prefix="stats"):
        super().__init__(handler, desc_prefix)

    def generate_menu(self):
        pass

    # TODO
    def generate_content(self):
        content = self.panel.content

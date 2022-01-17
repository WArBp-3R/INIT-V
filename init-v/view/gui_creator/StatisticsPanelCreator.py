from .PanelCreator import PanelCreator


class StatisticsPanelCreator(PanelCreator):
    TITLE = "Statistics"

    def __init__(self, desc_prefix="stats"):
        super().__init__(desc_prefix)

    def generate_menu(self):
        pass

    def generate_content(self):
        pass
        # TODO

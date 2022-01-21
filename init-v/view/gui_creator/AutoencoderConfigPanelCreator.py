import dash_core_components as dcc

from .PanelCreator import PanelCreator


class AutoencoderConfigPanelCreator(PanelCreator):
    TITLE = "Autoencoder Cfg."
    IS_OVERLAY = True

    def __init__(self, desc_prefix="ae_cfg"):
        super().__init__(desc_prefix)
        self.hidden_layer = None
        self.nodes_in_hidden_layer = None
        self.loss_function = None
        self.epochs = None
        self.optimizer = None

    def generate_menu(self):
        pass

    # TODO
    def generate_content(self):
        content = self.panel.content

import dash_core_components as dcc

from .AutoencoderConfigPanelCreator import AutoencoderConfigPanelCreator
from .PanelCreator import PanelCreator


class ConfigPanelCreator(PanelCreator):
    TITLE = "Configuration"

    def __init__(self, desc_prefix="cfg"):
        super().__init__(desc_prefix)
        self.length_scaling: dcc.Input
        self.value_scaling: dcc.Checklist
        self.normalization: dcc.RadioItems
        self.method: dcc.Checklist
        self.autoencoder_config_panel_creator: AutoencoderConfigPanelCreator

    def generate_menu(self):
        cfg_menu = self.panel.get_menu()
        cfg_menu.add_menu_item("autoencoder-config", "Autoencoder Cfg.")

    def generate_content(self):
        pass
        # TODO

    # callback
    def toggle_autoencoder_config_overlay(self, opn, cls):
        pass
        # TODO

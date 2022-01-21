import dash_core_components as dcc

from .AutoencoderConfigPanelCreator import AutoencoderConfigPanelCreator
from .PanelCreator import PanelCreator


class ConfigPanelCreator(PanelCreator):
    TITLE = "Configuration"

    def __init__(self, desc_prefix="cfg"):
        super().__init__(desc_prefix)
        self.length_scaling = None
        self.value_scaling = None
        self.normalization = None
        self.method = None

        self.add_sub_panel_creator(AutoencoderConfigPanelCreator())

    def generate_menu(self):
        cfg_menu = self.panel.get_menu()
        cfg_menu.add_menu_item("autoencoder-config", "Autoencoder Cfg.")

    def generate_content(self):
        content = self.panel.content

        # TODO - define content
        # self.length_scaling = None
        # self.value_scaling = None
        # self.normalization = None
        # self.method = None

        for spc in self.sub_panel_creators:
            spc.generate_content()

        content.components = [
                                 self.length_scaling,
                                 self.value_scaling,
                                 self.normalization,
                                 self.method,
                             ] + [spc.panel.layout for spc in self.sub_panel_creators]

    # callback
    def toggle_autoencoder_config_overlay(self, opn, cls):
        pass
        # TODO

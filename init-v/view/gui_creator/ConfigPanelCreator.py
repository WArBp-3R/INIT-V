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

        self.length_scaling = dcc.Input(id="length_scaling", type="number")
        self.value_scaling = dcc.Checklist(id="value_scaling",
                                           options=[
                                               {"label": "value scaling", "value": "VS"},
                                           ]
                                           )
        self.normalization = dcc.RadioItems(id="normalization",
                                            options=[
                                                {"label": "L1", "value": "L1"},
                                                {"label": "L2", "value": "L2"},
                                            ])
        self.method = dcc.Checklist(id="method",
                                    options=[
                                        {"label": "Autoencoder", "value": "AE"},
                                        {"label": "PCA", "value": "PCA"},
                                    ],
                                    value=[""])

        for spc in self.sub_panel_creators:
            spc.generate_content()

        content.components = ["Length Scaling",
                              self.length_scaling,
                              "Value Scaling",
                              self.value_scaling,
                              "Normalization",
                              self.normalization,
                              "Method",
                              self.method
                              ] + [spc.panel.layout for spc in self.sub_panel_creators]

    # TODO - callback
    def toggle_autoencoder_config_overlay(self, opn, cls):
        pass

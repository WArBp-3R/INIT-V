import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from .AutoencoderConfigPanelCreator import AutoencoderConfigPanelCreator
from .PanelCreator import PanelCreator


class ConfigPanelCreator(PanelCreator):
    TITLE = "Configuration"

    def __init__(self, handler, desc_prefix="cfg"):
        super().__init__(handler, desc_prefix)
        self.config_hidden = dcc.Input(id=self.panel.format_specifier("config_hidden"), type="hidden", value="")

        # TODO - replace magic values with DEFAULT_CONFIG from controller
        self.sample_size = dcc.Input(id=self.panel.format_specifier("sample_size"), type="number", value=150)
        self.scaling = dcc.RadioItems(id=self.panel.format_specifier("scaling"),
                                      options=[
                                          {"label": "Length", "value": "Length"},
                                          {"label": "Value Length", "value": "ValueLength"},
                                      ],
                                      value="Length")
        self.normalization = dcc.RadioItems(id=self.panel.format_specifier("normalization"),
                                            options=[
                                                {"label": "None", "value": "None"},
                                                {"label": "L1", "value": "L1"},
                                                {"label": "L2", "value": "L2"},
                                            ],
                                            value="None")
        self.method = dcc.Checklist(id=self.panel.format_specifier("method"),
                                    options=[
                                        {"label": "Autoencoder", "value": "AE"},
                                        {"label": "PCA", "value": "PCA"},
                                    ],
                                    value=["AE", "PCA"])

        self.add_sub_panel_creator(AutoencoderConfigPanelCreator(handler))

        ae_cfg_spc: AutoencoderConfigPanelCreator = self.sub_panel_creators["ae-cfg"]
        self.cfg_list = [self.sample_size,
                         self.scaling,
                         self.normalization,
                         self.method,
                         ae_cfg_spc.hidden_layers,
                         ae_cfg_spc.nodes_in_hidden_layers,
                         ae_cfg_spc.loss_function,
                         ae_cfg_spc.epochs,
                         ae_cfg_spc.optimizer]

        self.cfg_outputs = [Output(c.id, "value") for c in self.cfg_list]
        self.cfg_inputs = [Input(c.id, "value") for c in self.cfg_list]
        self.cfg_stats = [State(c.id, "value") for c in self.cfg_list]

        self.define_callbacks()

    def generate_menu(self):
        cfg_menu = self.panel.get_menu()
        cfg_menu.add_menu_item("autoencoder-config", "Autoencoder Cfg.")

    def generate_content(self):
        content = self.panel.content

        for spc in self.sub_panel_creators.values():
            spc.generate_content()

        content.components = [self.config_hidden,
                              html.Div(["Sample size: ", self.sample_size]),
                              html.Div(["Scaling", self.scaling]),
                              html.Div(["Normalization", self.normalization]),
                              html.Div(["Method", self.method]),
                              ] + [spc.panel.layout for spc in self.sub_panel_creators.values()]

    def define_callbacks(self):
        super().define_callbacks()

        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(self.sub_panel_creators["ae-cfg"].panel.id, "style")],
            {
                Input(self.panel.get_menu()["autoencoder-config"].id,
                      "n_clicks"): (lambda x: [{"display": "flex"}], None),
                Input(self.sub_panel_creators["ae-cfg"].panel.get_close_btn().id,
                      "n_clicks"): (lambda x: [{"display": "none"}], None),
            },
            [{}]
        )

        for i in self.cfg_inputs:
            self.handler.cb_mgr.register_callback(
                self.update_config,
                [Output(self.config_hidden.id, "value")],
                i,
                self.cfg_stats,
                [""]
            )

    def update_config(self, changed_input, *args):
        cfg = self.handler.interface.parse_config(args[0], args[1], args[2], args[3], args[4], args[5],
                                                  args[6], args[7], args[8])
        self.handler.interface.update_config(cfg)
        return ""

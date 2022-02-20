import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from .AutoencoderConfigPanelCreator import AutoencoderConfigPanelCreator
from .PanelCreator import PanelCreator
from ..GUI_Handler import app, get_input_id


class ConfigPanelCreator(PanelCreator):
    TITLE = "Configuration"

    def __init__(self, handler, desc_prefix="cfg"):
        super().__init__(handler, desc_prefix)
        self.config_output = dcc.Input(id=self.panel.format_specifier("config_output"), type="hidden", value="")

        # TODO - replace magic values with DEFAULT_CONFIG from controller
        self.length_scaling = dcc.Input(id=self.panel.format_specifier("length_scaling"), type="number", value=150)
        self.value_scaling = dcc.Checklist(id=self.panel.format_specifier("value_scaling"),
                                           options=[
                                               {"label": "Value Scaling", "value": "VS"},
                                           ]
                                           , value=[]
                                           )
        self.normalization = dcc.RadioItems(id=self.panel.format_specifier("normalization"),
                                            options=[
                                                {"label": "None", "value": "None"},
                                                {"label": "L1", "value": "L1"},
                                                {"label": "L2", "value": "L2"},
                                            ])
        self.method = dcc.Checklist(id=self.panel.format_specifier("method"),
                                    options=[
                                        {"label": "Autoencoder", "value": "AE"},
                                        {"label": "PCA", "value": "PCA"},
                                    ],
                                    value=[]
                                    )

        self.add_sub_panel_creator(AutoencoderConfigPanelCreator(handler))

        ae_cfg_spc: AutoencoderConfigPanelCreator = self.sub_panel_creators["ae-cfg"]

        self.config_input = [
            Input(self.length_scaling.id, "value"),
            Input(self.value_scaling.id, "value"),
            Input(self.normalization.id, "value"),
            Input(self.method.id, "value"),
            Input(ae_cfg_spc.hidden_layers.id, "value"),
            Input(ae_cfg_spc.nodes_in_hidden_layers.id, "value"),
            Input(ae_cfg_spc.loss_function.id, "value"),
            Input(ae_cfg_spc.epochs.id, "value"),
            Input(ae_cfg_spc.optimizer.id, "value"),
        ]

        self.define_callbacks()

    def generate_menu(self):
        cfg_menu = self.panel.get_menu()
        cfg_menu.add_menu_item("autoencoder-config", "Autoencoder Cfg.")

    def generate_content(self):
        content = self.panel.content

        for spc in self.sub_panel_creators.values():
            spc.generate_content()

        content.components = [self.config_output,
                              html.Div(["Length Scaling: ", self.length_scaling]),
                              html.Div([self.value_scaling]),
                              html.Div(["Normalization: ", self.normalization]),
                              html.Div(["Method", self.method]),
                              ] + [spc.panel.layout for spc in self.sub_panel_creators.values()]

    def define_callbacks(self):
        app.callback(
            Output(self.sub_panel_creators["ae-cfg"].panel.id, "style"),
            Input(self.panel.get_menu()["autoencoder-config"].id, "n_clicks"),
            Input(self.sub_panel_creators["ae-cfg"].panel.get_close_btn().id, "n_clicks"),
        )(self.toggle_autoencoder_config_overlay)

        app.callback(
            Output(self.panel.format_specifier("config_output"), "value"),
            self.config_input
        )(self.update_config)

    # CALLBACKS
    def toggle_autoencoder_config_overlay(self, opn, cls):
        button_id = get_input_id()
        print("toggle_ae-overlay")
        result = {}
        if button_id == self.panel.get_menu()["autoencoder-config"].id:
            result = {"display": "flex"}
        elif button_id == self.sub_panel_creators["ae-cfg"].panel.get_close_btn().id:
            result = {"display": "none"}
        else:
            pass
        return result

    def update_config(self, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        print("update-config")
        self.handler.interface.update_config(
            self.handler.interface.get_config(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt))
        return ""

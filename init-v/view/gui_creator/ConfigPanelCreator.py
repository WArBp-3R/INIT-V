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
        self.length_scaling = None
        self.value_scaling = None
        self.normalization = None
        self.method = None

        self.add_sub_panel_creator(AutoencoderConfigPanelCreator(handler))

        self.define_callbacks()

    def define_callbacks(self):
        app.callback(
            Output(self.sub_panel_creators["ae-cfg"].panel.id, "style"),
            Input(self.panel.get_menu()["autoencoder-config"].id, "n_clicks"),
            Input(self.sub_panel_creators["ae-cfg"].panel.get_close_btn().id, "n_clicks"),
        )(self.toggle_autoencoder_config_overlay)

    def generate_menu(self):
        cfg_menu = self.panel.get_menu()
        cfg_menu.add_menu_item("autoencoder-config", "Autoencoder Cfg.")

    def generate_content(self):
        content = self.panel.content

        self.length_scaling = dcc.Input(id="length_scaling", type="number")
        self.value_scaling = dcc.Checklist(id="value_scaling",
                                           options=[
                                               {"label": "Value Scaling", "value": "VS"},
                                           ])
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
                                    value=[])

        for spc in self.sub_panel_creators.values():
            spc.generate_content()

        content.components = [html.Div(["Length Scaling: ", self.length_scaling]),
                              html.Div([self.value_scaling]),
                              html.Div(["Normalization: ", self.normalization]),
                              html.Div(["Method", self.method]),
                              ] + [spc.panel.layout for spc in self.sub_panel_creators.values()]

    def toggle_autoencoder_config_overlay(self, opn, cls):
        print("toggle_autoencoder_config_overlay")
        button_id = get_input_id()
        result = {}
        if button_id == self.panel.get_menu()["autoencoder-config"].id:
            result = {"display": "flex"}
        elif button_id == self.sub_panel_creators["ae-cfg"].panel.get_close_btn().id:
            result = {"display": "none"}
        else:
            pass
        return result

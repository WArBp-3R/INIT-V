import dash_core_components as dcc
import dash_html_components as html

from .PanelCreator import PanelCreator


class AutoencoderConfigPanelCreator(PanelCreator):
    TITLE = "Autoencoder Cfg."
    IS_OVERLAY = True

    def __init__(self, handler, desc_prefix="ae-cfg"):
        super().__init__(handler, desc_prefix)
        # TODO - replace magic values with DEFAULT_CONFIG from controller
        self.hidden_layers = dcc.Input(id=self.panel.format_specifier("hidden_layers"),
                                       type="number",
                                       value=4)
        self.nodes_in_hidden_layers = dcc.Input(id=self.panel.format_specifier("nodes_in_hidden_layers"),
                                                type="text",
                                                value="256, 64, 32, 8")
        self.loss_function = dcc.RadioItems(id=self.panel.format_specifier("loss_function"),
                                            options=[
                                                {"label": "MSE", "value": "MSE"},
                                                {"label": "MAE", "value": "MAE"},
                                            ],
                                            value="MSE")
        self.epochs = dcc.Input(id=self.panel.format_specifier("epochs"),
                                type="number",
                                value=100)
        self.optimizer = dcc.Dropdown(id=self.panel.format_specifier("optimizer"),
                                      options=[
                                          {"label": "adam", "value": "adam"}
                                      ],
                                      value="adam")

    def generate_menu(self):
        pass

    def generate_content(self):
        content = self.panel.content

        content.components = [
            html.Div(["Number of hidden layers: ", self.hidden_layers]),
            html.Div(["Number of nodes in hidden layers: ", self.nodes_in_hidden_layers]),
            html.Div(["Loss function: ", self.loss_function]),
            html.Div(["Number of epochs for the training: ", self.epochs]),
            html.Div(["Optimizer: ", self.optimizer]),
        ]

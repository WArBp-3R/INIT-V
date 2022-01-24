import dash_core_components as dcc
import dash_html_components as html

from .PanelCreator import PanelCreator


class AutoencoderConfigPanelCreator(PanelCreator):
    TITLE = "Autoencoder Cfg."
    IS_OVERLAY = True

    def __init__(self, desc_prefix="ae_cfg"):
        super().__init__(desc_prefix)
        self.hidden_layers = None
        self.nodes_in_hidden_layers = None
        self.loss_function = None
        self.epochs = None
        self.optimizer = None

    def generate_menu(self):
        pass

    def generate_content(self):
        content = self.panel.content

        self.hidden_layers = dcc.Input(id="hidden_layer", type="number")
        self.nodes_in_hidden_layers = dcc.Input(id="nodes_in_hidden_layers", type="text")
        self.loss_function = dcc.RadioItems(id="loss_function",
                                            options=[
                                                {"label": "MSE", "value": "MSE"},
                                                {"label": "MAE", "value": "MAE"},
                                            ])
        self.epochs = dcc.Input(id="epochs", type="number")
        self.optimizer = dcc.Dropdown(id="epochs",
                                      options=[
                                          {"label": "adam", "value": "adam"}
                                      ])

        content.components = [
            html.Div(["Number of hidden layers: ", self.hidden_layers]),
            html.Div(["Number of nodes in hidden layers: ", self.nodes_in_hidden_layers]),
            html.Div(["Loss function: ", self.loss_function]),
            html.Div(["Number of epochs for the training: ", self.epochs]),
            html.Div(["Number of optimizer: ", self.optimizer]),
        ]

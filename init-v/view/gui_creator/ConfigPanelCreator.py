import os
from tkinter import filedialog as fd, simpledialog as sd

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from .PanelCreator import PanelCreator


class ConfigPanelCreator(PanelCreator):
    TITLE = "Configuration"

    def __init__(self, handler, desc_prefix="cfg"):
        self.config_hidden = None
        self.run_config_error_status = None
        self.sample_size = None
        self.scaling = None
        self.normalization = None
        self.method = None
        self.number_of_hidden_layers = None
        self.nodes_of_hidden_layers = None
        self.loss_function = None
        self.epochs = None
        self.optimizer = None

        # Dash dependencies
        self.cfg_list = None
        self.cfg_outputs = None
        self.cfg_inputs = None
        self.cfg_stats = None

        super().__init__(handler, desc_prefix)

    def generate_menu(self):
        cfg_menu = self.panel.get_menu()

        settings_dd_menu = cfg_menu.add_menu_item("settings", "Settings").set_dropdown().set_menu()
        settings_dd_menu.add_menu_item("get-default-config", "Get Default Config")
        settings_dd_menu.add_menu_item("change-default-config", "Change Default Config")
        settings_dd_menu.add_menu_item("load-config", "Load Config")
        settings_dd_menu.add_menu_item("save-config", "Save Config")
        settings_dd_menu.add_menu_item("export-config", "Export Config")

    def generate_content(self):
        self.config_hidden = dcc.Input(id=self.panel.format_specifier("config_hidden"), type="hidden", value="")
        self.run_config_error_status = html.Div(id="error_status")  # , children="", style={"display": "none"})

        self.sample_size = dcc.Input(id=self.panel.format_specifier("sample_size"), type="number")
        self.scaling = dcc.RadioItems(id=self.panel.format_specifier("scaling"),
                                      options=[
                                          {"label": "Length", "value": "Length"},
                                          {"label": "Value Length", "value": "ValueLength"},
                                      ])
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
                                    ])
        self.number_of_hidden_layers = dcc.Input(id=self.panel.format_specifier("number_of_hidden_layers"),
                                                 type="number")
        self.nodes_of_hidden_layers = dcc.Input(id=self.panel.format_specifier("nodes_of_hidden_layers"),
                                                type="text")
        self.loss_function = dcc.RadioItems(id=self.panel.format_specifier("loss_function"),
                                            options=[
                                                {"label": "MSE", "value": "MSE"},
                                                {"label": "MAE", "value": "MAE"},
                                            ])
        self.epochs = dcc.Input(id=self.panel.format_specifier("epochs"),
                                type="number")
        self.optimizer = dcc.Dropdown(id=self.panel.format_specifier("optimizer"),
                                      options=[
                                          {"label": "adam", "value": "adam"}
                                      ])

        self.panel.content.components = [self.config_hidden,
                                         self.run_config_error_status,
                                         html.Div(["Sample size: ", self.sample_size]),
                                         html.Div(["Scaling", self.scaling]),
                                         html.Div(["Normalization", self.normalization]),
                                         html.Div(["Method", self.method]),
                                         html.H3("Autoencoder Configuration: "),
                                         html.Div(["Hidden layers: ", self.number_of_hidden_layers]),
                                         html.Div(["Nodes in hidden layers: ", self.nodes_of_hidden_layers]),
                                         html.Div(["Loss function: ", self.loss_function]),
                                         html.Div(["Epochs for the training: ", self.epochs]),
                                         html.Div(["Optimizer: ", self.optimizer]),
                                         ]

    def define_callbacks(self):
        super().define_callbacks()

        self.cfg_list = [self.sample_size,
                         self.scaling,
                         self.normalization,
                         self.method,
                         self.number_of_hidden_layers,
                         self.nodes_of_hidden_layers,
                         self.loss_function,
                         self.epochs,
                         self.optimizer]
        self.cfg_outputs = [Output(c.id, "value") for c in self.cfg_list]
        self.cfg_inputs = [Input(c.id, "value") for c in self.cfg_list]
        self.cfg_stats = [State(c.id, "value") for c in self.cfg_list]

        settings_dd_menu = self.panel.get_menu()["settings"].dropdown.menu

        for i in self.cfg_inputs:
            self.handler.cb_mgr.register_callback(
                [Output(self.config_hidden.id, "value")],
                i,
                self.update_config,
                self.cfg_stats,
            )

        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(self.config_hidden.id, "value")], {
                Input(settings_dd_menu["change-default-config"].id,
                      "n_clicks"): (self.set_default_config, None),
                Input(settings_dd_menu["save-config"].id,
                      "n_clicks"): (self.save_config, None),
                Input(settings_dd_menu["export-config"].id,
                      "n_clicks"): (self.export_config, None),
            },
            [""]
        )

        self.handler.cb_mgr.register_multiple_callbacks(
            self.cfg_outputs, {
                Input(settings_dd_menu["get-default-config"].id,
                      "n_clicks"): (self.get_default_config, None),
                Input(settings_dd_menu["load-config"].id,
                      "n_clicks"): (self.load_config, None)
            },
            self.get_default_config(None)
        )

    # CALLBACK METHODS
    def update_config(self, changed_input, *args):
        cfg = self.handler.interface.parse_config(args[0], args[1], args[2], args[3], args[4], args[5],
                                                  args[6], args[7], args[8])
        self.handler.interface.update_config(cfg)
        return None

    def get_default_config(self, button):
        return list(self.handler.interface.unpack_config(self.handler.interface.get_default_config()))

    def set_default_config(self, button):
        try:
            self.handler.interface.set_default_config(self.handler.interface.get_active_config())
        except (AttributeError):
            # TODO implement visual key
            pass
        return None

    def save_config(self, button):
        name = self.handler.atomic_tk(sd.askstring, title="Load Config", prompt="Enter config name:")
        try:
            self.handler.interface.save_config(name + ".csv", self.handler.interface.get_active_config())
        except(AttributeError):
            # TODO implement visual key
            pass
        return None

    def load_config(self, button):
        path = self.handler.atomic_tk(fd.askopenfilename,
                                      title="Select config file.",
                                      filetypes=[("Config file", ".csv")],
                                      initialdir=os.path.abspath("../../out/Configurations/"))
        cfg = self.handler.interface.load_config(path)
        return list(self.handler.interface.unpack_config(cfg))

    def export_config(self, button):
        save_directory = self.handler.atomic_tk(fd.asksaveasfilename,
                                                title="Select save location.",
                                                filetypes=[("Config file", ".csv")])
        self.handler.interface.save_config(save_directory, self.handler.interface.get_active_config())
        return None

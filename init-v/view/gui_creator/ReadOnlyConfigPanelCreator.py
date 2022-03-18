import dash_html_components as html

from .PanelCreator import PanelCreator


class ReadOnlyConfigPanelCreator(PanelCreator):
    TITLE = "Run Configurations"

    def __init__(self, handler, desc_prefix="ro-cfg"):
        self.configs_table = None
        self.configs_tbody = None

        self.config_output_sink_register = dict()

        super().__init__(handler, desc_prefix)

    def generate_content(self):
        self.configs_tbody = html.Tbody(id=self.panel.format_specifier("configs_tbody"))

        self.configs_table = html.Table(id=self.panel.format_specifier("configs_table"), className="configtable",
                                        children=[
                                            html.Thead(children=[
                                                html.Tr(children=[
                                                    html.Th(colSpan=2, children="Run Info"),
                                                    html.Th(colSpan=2, children="Methods"),
                                                    html.Th(colSpan=3, children="Configuration"),
                                                    html.Th(colSpan=5, children="Autoencoder Configuration")
                                                ]),
                                                html.Tr(children=[
                                                    html.Th("#ID"),
                                                    html.Th("Timestamp"),
                                                    html.Th("AE"),
                                                    html.Th("PCA"),
                                                    html.Th("Smpl. size"),
                                                    html.Th("Scaling"),
                                                    html.Th("Nrm."),
                                                    html.Th("H. Layers"),
                                                    html.Th("N. in H. layers"),
                                                    html.Th("Loss func"),
                                                    html.Th("Epochs"),
                                                    html.Th("Opt."),
                                                    # html.Th("Set As Default"),
                                                    # html.Th("Save Config"),
                                                    # html.Th("Export Config")
                                                ])
                                            ]),
                                            self.configs_tbody
                                        ])

        self.panel.content.components = [self.configs_table]

    def define_callbacks(self):
        super().define_callbacks()

    # CALLBACK METHODS
    def display_config(self, runs):
        configs = self.handler.interface.get_run_configs(runs)
        result = list()
        for r, c in zip(sorted(runs), configs):
            ae_cfg = c.autoencoder_config
            row_id = self.panel.format_specifier(f"config-{r}")
            result.append(html.Tr(id=row_id, children=[
                html.Th(r),
                html.Td(self.handler.interface.get_run_list()[int(r)]),
                html.Td("X" if c.autoencoder else ""),
                html.Td("X" if c.pca else ""),
                html.Td(c.sample_size),
                html.Td(c.scaling),
                html.Td(c.normalization),
                html.Td(ae_cfg.number_of_hidden_layers),
                html.Td(", ".join([str(x) for x in ae_cfg.nodes_of_hidden_layers])),
                html.Td(ae_cfg.loss_function),
                html.Td(ae_cfg.number_of_epochs),
                html.Td(ae_cfg.optimizer),
                # html.Td(InteractElement(f"{row_id}-set-default", "Set As Default").layout),
                # html.Td(InteractElement(f"{row_id}-save", "Save Config").layout),
                # html.Td(InteractElement(f"{row_id}-export", "Export Config").layout)
            ]))

        return [result] if len(result) > 0 else None

    # def set_default_config(self, button, run, state):
    #     self.handler.interface.set_default_config(self.handler.interface.get_run_configs(run)[0])
    #     return state
    #
    # def save_config(self, button, run, state):
    #     name = self.handler.atomic_tk(sd.askstring, title="Load Config", prompt="Enter config name:")
    #     self.handler.interface.save_config(name + ".csv", self.handler.interface.get_run_configs(run)[0])
    #     return state
    #
    # def export_config(self, button, run, state):
    #     save_directory = self.handler.atomic_tk(fd.asksaveasfilename,
    #                                             title="Select save location.",
    #                                             filetypes=[("Config file", ".csv")])
    #     self.handler.interface.save_config(save_directory, self.handler.interface.get_run_configs(run)[0])
    #     return state

from datetime import datetime
import logging
import dash_cytoscape as cyto

from controller.init_v_controll_logic import ExportOptions
from controller.init_v_controll_logic.ControllerInterface import ControllerInterface
from model.AutoencoderConfiguration import AutoencoderConfiguration
from model.Configuration import Configuration
from model.RunResult import RunResult
from model.Session import Session
from model.Statistics import Statistics
from model.network.NetworkTopology import NetworkTopology
from view.GUI_Handler import GUIHandler
from view.ViewInterface import ViewInterface


class ViewAdapter(ViewInterface):
    _GUIHandler = None
    _Controller = None
    _runList = None

    def __init__(self, controller: ControllerInterface):
        """initializing method"""
        self.create_view(controller)
        logging.debug('viewadapter initalized')

    def create_view(self, controller: ControllerInterface):
        self._Controller = controller
        self._GUIHandler = GUIHandler(self)
        logging.debug('view created')

    def start_view(self):
        self._GUIHandler.run_app()
        logging.debug('app started')

    def parse_config(self, smp: int, scl: str, nrm: str, mtd: list[str], hly: int, nhl: str, lsf: str, epc: int,
                     opt: str) -> Configuration:
        try:
            nodes_of_hidden_layers = [int(s) for s in tuple(nhl.split(','))]
        except(Exception):
            nodes_of_hidden_layers = [-1]
        ae_config = AutoencoderConfiguration(hly, nodes_of_hidden_layers, lsf, epc, opt)
        config = Configuration("AE" in mtd, "PCA" in mtd, smp, scl, nrm, ae_config)
        return config

    def unpack_config(self, cfg: Configuration):
        mtd = []
        if cfg.autoencoder:
            mtd.append("AE")
        if cfg.pca:
            mtd.append("PCA")
        ae_cfg = cfg.autoencoder_config
        nhl = ", ".join([str(x) for x in ae_cfg.nodes_of_hidden_layers])
        return cfg.sample_size, cfg.scaling, cfg.normalization, mtd, ae_cfg.number_of_hidden_layers, nhl, ae_cfg.loss_function, ae_cfg.number_of_epochs, ae_cfg.optimizer

    def get_active_config(self) -> Configuration:
        return self._Controller.get_active_config()

    def update_config(self, config: Configuration):
        self._Controller.update_config(config)

    def is_active_config_valid(self) -> bool:
        return True if self.get_active_config().is_valid() else False

    def create_run(self) -> id:
        config: Configuration = self.get_active_config()
        return self._Controller.create_run(config)

    def get_run_list(self) -> list[datetime]:
        run_list = self._Controller.get_run_list()
        return [x.timestamp for x in run_list]

    def get_run_configs(self, runs) -> list[Configuration]:
        run_list = self._Controller.get_run_list()
        selected_run_list = [run_list[int(x)] for x in runs]
        configs = [x.config for x in selected_run_list]
        return configs

    def get_method_results(self, runs) -> list[(list[(float, float, str, str)], list[(float, float, str, str)])]:
        run_list = self._Controller.get_run_list()
        selected_run_list = [run_list[int(x)] for x in runs]
        method_results = [(x.result.autoencoder_result, x.result.pca_result) for x in selected_run_list]
        return method_results

    def get_performance(self, runs) -> list[(dict[str, list], list[(float, float)])]:
        run_list = self._Controller.get_run_list()
        selected_run_list = [run_list[int(x)] for x in runs]
        perf_results = [(x.analysis.autoencoder, x.analysis.pca) for x in selected_run_list]
        return perf_results

    def get_statistics(self) -> Statistics:
        return self._Controller.get_statistics()

    def get_network_topology(self) -> NetworkTopology:
        return self._Controller.get_network_topology()

    def get_highest_protocol_set(self) -> set[str]:
        return self._Controller.get_highest_protocols()

    def get_pcap_name(self) -> str:
        return self._Controller.get_pcap_name()

    # cleanup bookmark
    """loads the data of the given runs"""

    def compare_runs(self, pos: list) -> list[RunResult]:
        return self._Controller.compare_runs(pos)

    def create_new_session(self, pcap_path: str):
        return self._Controller.create_new_session(pcap_path)

    """loads a session from source_paths"""

    def load_session(self, source_path: str) -> Session:
        return self._Controller.load_session(source_path)

    """loads a config file from the source_path"""

    def load_config(self, source_path: str) -> Configuration:
        return self._Controller.load_config(source_path)

    """loads topology graph from source_path"""

    def load_topology_graph(self, source_path: str) -> cyto.Cytoscape:
        return self._Controller.load_topology_graph(source_path)

    """saves the session with the config from the given values as active config to output path"""

    def save_session(self, output_path: str, t_g: cyto.Cytoscape):
        self._Controller.save_session(output_path, t_g)

    """saves the config from the given values to output path"""

    def save_config(self, output_path: str, config: Configuration):
        self._Controller.save_config(output_path, config)

    def get_default_config(self) -> Configuration:
        return self._Controller.get_default_config()

    def set_default_config(self, config: Configuration):
        self._Controller.set_default_config(config)

    """exports the content specified in options to output_path"""

    def export(self, output_path: str, options: ExportOptions):
        self._Controller.export(output_path, options)

    def get_session_path(self):
        session = self._Controller.get_session()
        return session.pcap_path if session else None

    def get_workspace_path(self):
        return self._Controller.get_workspace_path()

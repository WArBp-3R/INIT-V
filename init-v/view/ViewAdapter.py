from model.network.NetworkTopology import NetworkTopology
from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from model.RunResult import RunResult
from model.Session import Session
from controller.init_v_controll_logic import ExportOptions
from controller.init_v_controll_logic.ControllerInterface import ControllerInterface
from view.ViewInterface import ViewInterface
from view.GUI_Handler import GUIHandler
from keras.callbacks import History
from model.IStatistic import IStatistic
from datetime import datetime
import dash_cytoscape as cyto

class ViewAdapter(ViewInterface):
    _GUIHandler = None
    _Controller = None
    _runList = None

    """creates the page"""

    def create_view(self, controller: ControllerInterface):
        self._Controller = controller
        self._GUIHandler = GUIHandler(self)

    """initializing method"""

    def __init__(self, controller: ControllerInterface):
        self.create_view(controller)

    """builds a config from the given values"""

    @staticmethod
    def get_config(lsc: int, vsc: list[str], nrm: str, mtd: list[str], hly: int, nhl: str, lsf: str, epc: int,
                   opt: str) -> Configuration:
        aut_config = AutoencoderConfiguration(hly, [int(s) for s in tuple(nhl.split(','))], lsf, epc, opt)
        config = Configuration("AE" in mtd, "PCA" in mtd, lsc, "VS" in vsc, nrm, aut_config)
        return config

    """returns the list of runs represented by timestamps"""

    def get_run_list(self) -> list[datetime]:
        run_list = self._Controller.get_run_list()
        return [x.timestamp for x in run_list]

    def get_real(self):
        return self._Controller.get_run_list()

    def get_method_results(self, run) -> (list[(float, float, str)], list[(float, float, str)]):
        run_list = self._Controller.get_run_list()
        method_results = self._Controller.get_run_list()[run].result
        return method_results.autoencoder_result, method_results.pca_result

    def get_performance(self, run) -> list[(float, float)]:
        run_list = self._Controller.get_run_list()
        perf_results = self._Controller.get_run_list()[run].analysis
        return perf_results.pca

    """creates a new run from the given config values and returns its"""
    def create_run(self, config: Configuration) -> RunResult:
        #config: Configuration = self.get_config(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt)
        return self._Controller.create_run(config)

    """returns the current network topology"""
    def get_network_topology(self) -> NetworkTopology:
        return self._Controller.get_network_topology()

    """returns all used protocols"""
    def get_highest_protocol_set(self) -> set[str]:
        return self._Controller.get_highest_protocols()

    """loads the data of the given runs"""
    def compare_runs(self, pos: list) -> list[RunResult]:
        return self._Controller.compare_runs(pos)

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
    def save_session(self, output_path: str, config: Configuration, t_g: cyto.Cytoscape):
        self._Controller.save_session(output_path, config, t_g)

    """saves the config from the given values to output path"""
    def save_config(self, output_path: str, config: Configuration):
        self._Controller.save_config(output_path, config)

    """exports the content specified in options to output_path"""
    def export(self, output_path: str, options: ExportOptions):
        self._Controller.export(output_path, options)

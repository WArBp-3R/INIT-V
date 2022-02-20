from model.network.NetworkTopology import NetworkTopology
from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from controller.init_v_controll_logic import ExportOptions
from controller.init_v_controll_logic.ControllerInterface import ControllerInterface
from view.ViewInterface import ViewInterface
from view.GUI_Handler import GUIHandler
from keras.callbacks import History
from model.IStatistic import IStatistic
from datetime import datetime


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

    """creates a new run from the given config values and writes its data to the panels"""

    def create_run(self, lsc: int, vsc: list[str], nrm: str, mtd: list[str], hly: int, nhl: str, lsf: str, epc: int,
                   opt: str):
        pca_result: list[(float, float, str)] = []
        pca_performance: list[(float, float)] = []
        autoencoder_result: list[(float, float, str)] = []
        autoencoder_performance: list[History] = []
        timestamp: list[datetime] = []
        stats: list[IStatistic] = []
        topology: list[NetworkTopology] = []

        config: Configuration = self.get_config(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt)

        self._Controller.create_run(pca_performance, pca_result, autoencoder_performance, autoencoder_result, topology,
                                    timestamp, stats, [config])
        # now all values needed are set.

    def get_network_topology(self):
        return self._Controller.get_network_topology()

    def get_protocol_set(self) -> set[str]:
        protocol_set = set()
        for c in self.get_network_topology().connections:
            protocol_set.update(c.protocols)
        return protocol_set

    """loads the data of the given runs into the compare panels"""

    def compare_runs(self, pos: list):
        pca_results: list[list[(float, float, str)]] = []
        pca_performances: list[list[(float, float)]] = []
        autoencoder_results: list[list[(float, float, str)]] = []
        autoencoder_performances: list[History] = []
        timestamps: list[datetime] = []
        stats: list[list[IStatistic]] = []
        topology: list[NetworkTopology] = []
        configs: list[Configuration] = []
        self._Controller.compare_runs(pos, pca_results, pca_performances, autoencoder_performances, autoencoder_results,
                                      timestamps, stats, topology, configs)
        #now all values needed are set

    """loads a session from source_path and writes its content to the panels"""
    def load_session(self, source_path: str):
        pca_result: list[(float, float, str)] = []
        pca_performance:  list[(float, float)] = []
        autoencoder_result: list[(float, float, str)] = []
        autoencoder_performance: list[History] = []
        timestamp: list[datetime] = []
        stats: list[IStatistic] = []
        topology: list[NetworkTopology] = []
        config: list[Configuration] = []
        self._Controller.load_session(source_path, pca_performance, pca_result, autoencoder_performance,
                                      autoencoder_result, topology, timestamp, stats, config)
        #write data to panels

    """loads a config file from the source_path into the model and config panel"""
    def load_config(self, source_path: str):
        config = self._Controller.load_config(source_path)
        #write config to panel

    def create_new_session(self, pcap_path:str):
        topology = []
        config = []
        self._Controller.create_new_session(pcap_path, topology, config)

        #write config and topology to panel.


    """saves the session with the config from the given values as active config to output path"""
    # def save_session(self, output_path: str, lsc: int, vsc: list[str], nrm: str, mtd: list[str], hly: int, nhl: str,
    #                  lsf: str, epc: int, opt: str):
    #     self._Controller.save_session(output_path, self.get_config(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt))
    def save_session(self, output_path: str, config: Configuration):
        self._Controller.save_session(output_path, config)


    def update_config(self, config: Configuration):
        self._Controller.update_config(config)
        pass

    """saves the config from the given values to output path"""
    def save_config(self, output_path: str):
        self._Controller.save_config(output_path, None)

    def set_default_config(self, lsc: int, vsc: list[str], nrm: str, mtd: list[str], hly: int, nhl: str,
                    lsf: str, epc: int, opt: str):
        self._Controller.set_default_config(self.get_config(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt))
        pass

    def default_config(self):
        config = self._Controller.default_config()
        #write config to panel

    """exports the content specified in options to output_path"""
    def export(self, output_path: str, options: ExportOptions):
        self._Controller.export(output_path, options)

from model.network.NetworkTopology import NetworkTopology
from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from controller.init_v_controll_logic import ExportOptions
from controller.init_v_controll_logic import ControllerInterface
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
    def create_view(self, controller: ControllerInterface.ControllerInterface):
        self._GUIHandler = GUIHandler()
        self._Controller = controller
        self._GUIHandler.get_layout()

    """initializing method"""
    def __init__(self, controller: ControllerInterface.ControllerInterface):
        self.create_view(controller)

    """builds a config from the given values"""
    @staticmethod
    def get_config(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt) -> Configuration:
        aut_config = AutoencoderConfiguration(hly, nhl, lsf, epc, opt)
        config = Configuration(mtd, vsc, lsc, nrm, aut_config)
        return config

    """returns the list of runs represented by timestamps"""
    def get_run_list(self) -> list:
        return self._Controller.get_run_list()

    """creates a new run from the given config values and writes its data to the panels"""
    def create_run(self, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        pca_result: list = []
        pca_performance: list = []
        autoencoder_result: list = []
        autoencoder_performance:list = []
        timestamp: list = []
        stats: list = []
        topology: list = []

        config = self.get_config(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt)

        self._Controller.create_run(pca_performance, pca_result, autoencoder_performance, autoencoder_result, topology,
                                    timestamp, stats, config)
        #now all values needed are set.

    """loads the data of the given runs into the compare panels"""
    def compare_runs(self, pos: list):
        pca_results: list = []
        pca_performances: list = []
        autoencoder_results: list = []
        autoencoder_performances: list = []
        timestamps: list = []
        stats: list = []
        topology: list = []
        configs: list = []
        self._Controller.compare_runs(pos, pca_results, pca_performances, autoencoder_performances, autoencoder_results,
                                      timestamps, stats, topology, configs)
        #now all values needed are set


    """loads a session from source_path and writes its content to the panels"""
    def load_session(self, source_path: str):
        pca_result: list = []
        pca_performance: list = []
        autoencoder_result: list = []
        autoencoder_performance: list = []
        timestamp: list = []
        stats: list = []
        topology: list = []
        config: list = []
        self._Controller.load_session(source_path, pca_performance, pca_result, autoencoder_performance,
                                      autoencoder_result, topology, timestamp, stats, config)
        #write data to panels

    """loads a config file from the source_path into the model and config panel"""
    def load_config(self, source_path: str):
        config = self._Controller.load_config(source_path)
        #write config to panel

    """saves the session with the config from the given values as active config to output path"""
    def save_session(self, output_path: str, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        self._Controller.save_session(output_path, self.get_config(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt))

    """saves the config from the given values to output path"""
    def save_config(self, output_path: str, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        self._Controller.save_config(output_path, self.get_config(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt))

    """exports the content specified in options to output_path"""
    def export(self, output_path: str, options: ExportOptions):
        self._Controller.export(output_path, options)

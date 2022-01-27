from model.network.NetworkTopology import NetworkTopology
from model import Configuration
from model import AutoencoderConfiguration
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
    
    def create_view(self, controller: ControllerInterface.ControllerInterface):
        self._GUIHandler = GUIHandler()
        self._Controller = controller
        self._GUIHandler.get_layout()

    def __init__(self, controller: ControllerInterface.ControllerInterface):
        self.create_view(controller)

    @staticmethod
    def get_config(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt) -> Configuration:
        aut_config = AutoencoderConfiguration(hly, nhl, lsf, epc, opt)
        config = Configuration(mtd, vsc, lsc, nrm, aut_config)
        return config

    def get_run_list(self) -> list:
        pass

    def create_run(self, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        pca_result: list
        pca_performance: list
        autoencoder_results: list
        autoencoder_performance:list
        timestamp: list
        stats: list
        topology: list

        config = self.get_config(lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt)

        self._Controller.create_run(pca_performance, pca_result, autoencoder_performance, autoencoder_results, topology,
                                    timestamp, stats, config)
        #now all values needed are set.

    #def update_compare_performance(self, pca_performances: list[list[(float, float)]],
    #                               autoencoder_performances: list[History], timestamps: list[datetime]):
    #    pass

    #def update_compare_methods(self, pca_results: list[list[(float, float)]],
    #                           autoencoder_results: list[list[(float, float)]], timestamps: list[datetime]):
    #   pass

    #def update_compare_statistics(self, stats: list[list[IStatistic]], timestamps: list[datetime]):
    #    pass
    #def update_compare_configuration(self, configs: list[Configuration], timestamps: list[datetime]):
    #    pass

    def compare_runs(self, pos: list):
        self._Controller.compare_runs(pos)

    def load_session(self, source_path: str):
        self._Controller.load_session(source_path)

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

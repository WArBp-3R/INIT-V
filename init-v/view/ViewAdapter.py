from model.network.NetworkTopology import NetworkTopology
from model import Configuration
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

    def get_config(self) -> Configuration:
        return None

    def get_run_list(self) -> list:
        pass

    def create_run(self):
        pca_result: list
        pca_performance: list
        autoencoder_results: list
        autoencoder_performance:list
        timestamp: list
        stats: list
        config: list
        topology: list

        self._Controller.create_run(pca_performance, pca_result, autoencoder_performance, autoencoder_results, topology, timestamp, stats, config)

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
        self._Controller.load_config(source_path)

    def save_session(self, output_path: str):
        self._Controller.save_session(output_path)

    def save_config(self, output_path: str):
        self._Controller.save_config(output_path)

    def export(self, output_path: str, options: ExportOptions):
        self._Controller.export(output_path, options)

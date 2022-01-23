from model.network.NetworkTopology import NetworkTopology
from model import Configuration
from controller.init_v_controll_logic import ExportOptions
from controller.init_v_controll_logic import ControllerInterface
from view.ViewInterface import ViewInterface
from view.GUI_Handler import GUIHandler
from keras.callbacks import History
from model.IStatistic import IStatistic


class ViewAdapter(ViewInterface):
    _GUIHandler = None
    _Controller = None

    def create_view(self, controller: ControllerInterface.ControllerInterface):
        self._GUIHandler = GUIHandler()
        self._Controller = controller
        self._GUIHandler.get_layout()

    def __init__(self, controller: ControllerInterface.ControllerInterface):
        self.create_view(controller)

    def update_performance(self, pca: list[(float, float)], autoencoder: History):
        pass

    def update_methods(self, pca_result: list[(float, float)], autoencoder_result: list[(float, float)]):
        pass

    def update_topology(self, topology: NetworkTopology):
        pass

    def update_statistics(self, stats: list[IStatistic]):
        pass

    def update_configuration(self, config: Configuration):
        pass

    def get_run_list(self) -> list:
        pass

    def create_run(self):
        self._Controller.create_run()

    def update_compare_performance(self, pca_performances: list[list[(float, float)]],
                                   autoencoder_performances: list[History], timestamps: list[int]):
        pass

    def update_compare_methods(self, pca_results: list[list[(float, float)]],
                               autoencoder_results: list[list[(float, float)]], timestamps: list[int]):
        pass

    def update_compare_statistics(self, stats: list[list[IStatistic]], timestamps: list[int]):
        pass

    def update_compare_configuration(self, configs: list[Configuration], timestamps: list[int]):
        pass

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

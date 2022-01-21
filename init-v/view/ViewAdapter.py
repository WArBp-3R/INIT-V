from model.network.NetworkTopology import NetworkTopology
from model import Configuration
from controller.init_v_controll_logic import ExportOptions
from view.ViewInterface import ViewInterface
from keras.callbacks import History
from model.IStatistic import IStatistic


class ViewAdapter(ViewInterface):

    def __init__(self):
        create_view()

    def create_view(self):
        pass

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
        pass

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
        pass

    def load_session(self, source_path: str):
        pass

    def load_config(self, source_path: str):
        pass

    def save_session(self, output_path: str):
        pass

    def save_config(self, output_path: str):
        pass

    def export(self, output_path: str, options: ExportOptions):
        pass

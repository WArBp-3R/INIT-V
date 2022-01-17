from model.network.NetworkTopology import NetworkTopology
from model import Configuration
from controller.init_v_controll_logic import ExportOptions


class ViewInterface:

    def create_view(self):
        pass
    def update_performance(self, pca: list, autoencoder: History):
        pass
    def update_methods(self, pca_result: list, autoencoder_result: list):
        pass
    def update_topology(self, topolgy: NetworkTopology):
        pass
    def update_statistics(self, stats : list):
        pass
    def update_configuration(self, config: Configuration):
        pass
    def get_run_list(self)->list:
        pass
    def create_run(self):
        pass
    def update_compare_performance(self, pca: list, autoencoder: History, pos:list):
        pass
    def update_compare_methods(self, pca_result: list, autoencoder_result: list, pos: list):
        pass
    def update_compare_statistics(self, stats : list, pos: list):
        pass
    def update_compare_configuration(self, config: Configuration, pos: list):
        pass

    def compare_runs(self, pos: list):
        pass
    def load_session(self, source_path: str):
        pass
    def load_config(self, source_path: str):
        pass
    def save_session(self, output_path: str):
        pass
    def save_sonfig(self, output_path: str):
        pass
    def export(self, output_path: str, options: ExportOptions):
        pass










from model.Configuration import Configuration
from model.RunResult import RunResult
from model.Session import Session
from controller.init_v_controll_logic.ExportOptions import ExportOptions
from controller.init_v_controll_logic.Settings import Settings


from model.Configuration import Configuration
from controller.init_v_controll_logic import ExportOptions
from model.Session import Session
from datetime import datetime
from keras.callbacks import History
from model.network.NetworkTopology import NetworkTopology
from model.IStatistic import IStatistic


class ControllerInterface:

    def startup(self):
        #TODO comment
        pass

    def update_topology(self):
        #TODO comment
        pass

    def create_run(self, pca_performance: list[(float, float)], pca_result: list[(float, float, str)],
                   autoencoder_performance: list[History], autoencoder_result: list[(float, float, str)],
                   topology: list[NetworkTopology], timestamp: list[datetime], stats: list[IStatistic],
                   config: list[Configuration]):
        #TODO comment
        pass

    def update_config(self, config: Configuration):
        #TODO comment
        pass

    def create_new_session(self, session: Session):
        #TODO comment
        pass
        
    def compare_runs(self, pos: list[int], pca_results: list[list[(float, float, str)]],
                     pca_performances: list[list[(float, float)]], autoencoder_performances: list[History],
                     autoencoder_results: list[list[(float, float, str)]],
                     timestamps: list[datetime], stats: list[list[datetime]], topology: list[NetworkTopology],
                     config: list[Configuration]):
        #TODO comment
        pass

    def load_session(self, source_path: str, pca_performance: list[(float, float)],
                     pca_result: list[(float, float, str)], autoencoder_performance: list[History],
                     autoencoder_result: list[(float, float, str)], topology: list[NetworkTopology],
                     timestamp: list[datetime], stats: list[IStatistic], config: list[Configuration]):
        #TODO comment
        pass

    def load_config(self, source_path: str) -> Configuration:
        #TODO comment
        pass

    def save_session(self, output_path: str, config: Configuration):
        #TODO comment
        pass

    def default_config(self) -> Configuration:
        pass

    def set_default_config(self, config: Configuration):
        pass

    def save_config(self, output_path: str, config: Configuration):
        #TODO comment
        pass

    def export(self, output_path: str, options: ExportOptions):
        # TODO comment
        pass

    def get_run_list(self) -> list[RunResult]:
        # TODO comment
        pass

    def get_network_topology(self) -> NetworkTopology:
        pass

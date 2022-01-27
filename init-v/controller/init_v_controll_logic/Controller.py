from controller.init_v_controll_logic.ControllerInterface import ControllerInterface
from model.Configuration import Configuration
from controller.init_v_controll_logic import ExportOptions
from model.Session import Session
from controller.init_v_controll_logic.Settings import Settings
from datetime import datetime
from keras.callbacks import History
from model.network.NetworkTopology import NetworkTopology
from model.IStatistic import IStatistic


class Controller (ControllerInterface):
    WORKSPACE_PATH: str
    # session: Session
    # settings: Settings

    def __init__(self, session: Session, settings: Settings):
        self.session = session
        self.settings = settings

    def startup(self):
        #TODO implement
        pass

    def update_topology(self):
        #TODO implement
        pass

    def create_run(self, pca_performance: list[(float, float)], pca_result: list[(float, float, str)],
                   autoencoder_performance: list[History], autoencoder_result: list[(float, float, str)],
                   topology: list[NetworkTopology], timestamp: list[datetime], stats: list[IStatistic],
                   config: list[Configuration]):
        #TODO implement
        #create run, save in model and update the given attributes, which are all!! lists.
        #if an object is not a list just do varX = [<object_not_being_a_list>]
        pass

    #def update_config(self, config: Configuration):
    #    #TODO implement
    #    pass

    def create_new_session(self, session: Session):
        # TODO implement
        pass

    def compare_runs(self, pos: list[int], pca_results: list[list[(float, float, str)]],
                     pca_performances: list[list[(float, float)]], autoencoder_performances: list[History],
                     autoencoder_results: list[list[(float, float, str)]],
                     timestamps: list[datetime], stats: list[list[datetime]], topology: list[NetworkTopology],
                     config: list[Configuration]):
        #TODO implement
        pass

    def load_session(self, source_path: str, pca_performance: list[(float, float)],
                     pca_result: list[(float, float, str)], autoencoder_performance: list[History],
                     autoencoder_result: list[(float, float, str)], topology: list[NetworkTopology],
                     timestamp: list[datetime], stats: list[IStatistic], config: list[Configuration]):
        #TODO implement
        #load session
        #save in session variable
        #update values, which are, again, all!! lists.
        pass

    def load_config(self, source_path: str) -> Configuration:
        #TODO implement
        #load config
        #write to model
        #return config
        pass

    def save_session(self, output_path: str, config: Configuration):
        #TODO implement
        #config is the active Configuration
        pass

    def save_config(self, output_path: str, config: Configuration):
        #TODO implement
        pass

    def export(self, output_path: str, options: ExportOptions):
        #TODO implement
        pass

    def get_run_list(self) -> list[datetime]:
        #TODO implement
        pass

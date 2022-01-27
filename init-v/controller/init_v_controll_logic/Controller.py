from controller.init_v_controll_logic.ControllerInterface import ControllerInterface
from model import Configuration
from controller.init_v_controll_logic import ExportOptions
from model.Session import Session
from controller.init_v_controll_logic.Settings import Settings

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

    def create_run(self, pca_performance, pca_result, autoencoder_performance, autoencoder_results, topology, timestamp,
                   stats, config):
        #TODO implement
        #create run, save in model and update the given attributes, wich are all!! lists.
        #if an object is not a list just do varX = [<object_not_being_a_list>]
        pass

    #def update_config(self, config: Configuration):
    #    #TODO implement
    #    pass

    def create_new_session(self, session: Session):
        # TODO implement
        pass



    def compare_runs(self, pos : list[int]):
        #TODO implement
        pass

    def load_session(self, source_path: str):
        #TODO implement
        pass

    def load_config(self, source_path: str):
        #TODO implement
        pass

    def save_session(self, output_path: str):
        #TODO implement
        pass

    def save_config(self, output_path: str):
        #TODO implement
        pass

    def export(self, output_path: str, options: ExportOptions):
        #TODO implement
        pass


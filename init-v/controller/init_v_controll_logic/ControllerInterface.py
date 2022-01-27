from model import Configuration
from controller.init_v_controll_logic import ExportOptions
from model.Session import Session

class ControllerInterface:

    def startup(self):
        #TODO comment
        pass

    def update_topology(self):
        #TODO comment
        pass

    def create_run(self, pca_performance, pca_result, autoencoder_performance, autoencoder_results, topology, timestamp, stats, config):
        #TODO comment
        pass

    def update_config(self, config: Configuration):
        #TODO comment
        pass

    def create_new_session(self, session: Session):
        #TODO comment
        pass

        
        
    def compare_runs(self, pos:list[int]):
        #TODO comment
        pass

    def load_session(self, source_path: str):
        #TODO comment
        pass

    def load_config(self, source_path: str):
        #TODO comment
        pass

    def save_session(self, output_path: str, config: Configuration):
        #TODO comment
        pass

    def save_config(self, output_path: str, config:Configuration):
        #TODO comment
        pass

    def export(self, output_path: str, options: ExportOptions):
        #TODO comment
        pass


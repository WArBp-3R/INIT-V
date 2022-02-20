from model_test.Configuration import *
from model_test.Session import *
from controller.init_v_controll_logic.ExportOptions import *

class FileManagerInterface:
    def load(self, source_path: str, option: str) -> Configuration:
        #TODO comment
        pass

    def load(self, source_path: str, option: str) -> Session:
        #TODO comment
        pass

    def save(self, output_path: str, session: Session):
        #TODO comment
        pass

    def save(self, output_path: str, config: Configuration):
        #TODO comment
        pass

    def export(self, output_path: str, session: Session, options: ExportOptions):
        #TODO comment
        pass

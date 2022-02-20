from controller.file_manager.SessionEncoder import SessionEncoder
from controller.file_manager.ConfigEncoder import ConfigEncoder
from model_test.Session import *

class FileSaver:
    def save(self, output_path: str, input: Session or Configuration):
        #TODO implement
        if isinstance(input, Session):
            e = SessionEncoder()
            e.save(output_path, input)
        elif isinstance(input, Configuration):
            e = ConfigEncoder()
            e.save(output_path, input)
        pass

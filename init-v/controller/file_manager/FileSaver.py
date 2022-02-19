from controller.file_manager.SessionEncoder import SessionEncoder
from controller.file_manager.ConfigEncoder import ConfigEncoder
from model.Session import *

class FileSaver:
    def save(self, output_path: str, input: Session or Configuration, *args):
        #TODO implement
        if isinstance(input, Session):
            e = SessionEncoder()
            e.save(output_path, input, args[0])
        elif isinstance(input, Configuration):
            e = ConfigEncoder()
            e.save(output_path, input)
        pass

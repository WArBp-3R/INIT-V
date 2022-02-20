from controller.file_manager.SessionEncoder import SessionEncoder
from controller.file_manager.ConfigEncoder import ConfigEncoder
from model.Session import *

class FileSaver:
    """
    method to decide if given input is a Configuration or a Session and call the right method

    :param  output_path: string of the output path.
    :param input: object `c`for a Configuration object, `s` for a Session object.
    """
    def save(self, output_path: str, input: Session or Configuration, *args):
        #TODO implement
        if isinstance(input, Session):
            e = SessionEncoder()
            e.save(output_path, input, args[0])
        elif isinstance(input, Configuration):
            e = ConfigEncoder()
            e.save(output_path, input)
        pass

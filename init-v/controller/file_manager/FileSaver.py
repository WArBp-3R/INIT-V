from SessionEncoder import SessionEncoder
from ConfigEncoder import ConfigEncoder
from model.Session import *

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

    # def save(self, output_path: str, config: Configuration):
    #     #TODO implement
    #     e = ConfigEncoder()
    #     e.save(output_path, config)
    #     pass

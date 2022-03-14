import logging

from controller.file_manager.SessionEncoder import SessionEncoder
from controller.file_manager.ConfigEncoder import ConfigEncoder
from model.Session import *


class FileSaver:

    def save(self, output_path: str, input: Session or Configuration, *args):
        """
        method to decide if given input is a Configuration or a Session and call the right method
        :param  output_path: string of the output path.
        :param input: object `c`for a Configuration object, `s` for a Session object.
        """
        if isinstance(input, Session):
            e = SessionEncoder()
            e.save(output_path, input, args[0])
            logging.debug('session detected in save')
        elif isinstance(input, Configuration):
            e = ConfigEncoder()
            e.save(output_path, input)
            logging.debug('configuration detected in save')
        pass

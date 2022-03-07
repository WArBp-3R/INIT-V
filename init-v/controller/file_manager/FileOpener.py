from model.Configuration import Configuration
from model.Session import Session

from controller.file_manager.ConfigDecoder import ConfigDecoder
from controller.file_manager.SessionDecoder import SessionDecoder


class FileOpener:

    def load(self, source_path: str, option: str) -> Configuration or Session:
        """
        method to decide if given input is a Configuration or a Session and call the right method
        :param  source_path: string of the source path.
        :param option: string `c`for a Configuration, `s` for a Session.
        """
        if option == "c":
            opener = ConfigDecoder()
            return opener.load_configuration(source_path)
        elif option == "s":
            opener = SessionDecoder()
            return opener.load_session(source_path)
        elif option == "t":
            opener = SessionDecoder()
            return opener.load_t_graph(source_path)
        pass

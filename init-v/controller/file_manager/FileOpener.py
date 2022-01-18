from model.Configuration import Configuration
from model.Session import Session

from controller.file_manager.ConfigDecoder import ConfigDecoder
from controller.file_manager.SessionDecoder import SessionDecoder

class FileOpener:
    def load(self, source_path: str, option: str) -> Configuration or Session:
        if option == "c":
            opener = ConfigDecoder()
            return opener.load_configuration(source_path)
        elif option == "s":
            opener = SessionDecoder()
            return opener.load_session(source_path)
        pass


    # old with method overloading
    # def load(self, source_path: str, option: str) ->  Session:
    #     pass

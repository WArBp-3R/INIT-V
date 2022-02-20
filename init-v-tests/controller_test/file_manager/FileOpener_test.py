from model_test.Configuration import Configuration
from model_test.Session import Session

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



from controller.file_manager.FileManagerInterface import FileManagerInterface
from controller.file_manager.FileSaver import FileSaver
from controller.file_manager.FileOpener import FileOpener
from controller.file_manager.ExportCreator import ExportCreator
from controller.init_v_controll_logic.ExportOptions import ExportOptions

from model_test.ModelInterface import ModelInterface
from model_test.network.NetworkTopology import NetworkTopology
from model_test.Configuration import Configuration
from model_test.RunResult import RunResult
from model_test.Session import Session
from model_test.AutoencoderConfiguration import AutoencoderConfiguration



class FileManager(FileManagerInterface):
    def load(self, source_path: str, option: str) -> Configuration or Session:
        #TODO test
        opener = FileOpener()
        return opener.load(source_path, option)
        pass

    def save(self, output_path: str, input: Configuration or Session):
        #TODO test
        saver = FileSaver()
        saver.save(output_path, input)


        pass

    def export(self, output_path: str, session: Session, options: ExportOptions):
        #TODO implement
        ExportCreator.export(output_path, session, options)
        pass

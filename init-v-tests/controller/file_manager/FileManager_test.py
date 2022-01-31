

from controller.file_manager.FileManagerInterface import FileManagerInterface
from controller.file_manager.FileSaver import FileSaver
from controller.file_manager.FileOpener import FileOpener
from controller.file_manager.ExportCreator import ExportCreator
from controller.init_v_controll_logic.ExportOptions import ExportOptions

from model.ModelInterface import ModelInterface
from model.network.NetworkTopology import NetworkTopology
from model.Configuration import Configuration
from model.RunResult import RunResult
from model.Session import Session
from model.AutoencoderConfiguration import AutoencoderConfiguration



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

import dash_cytoscape as cyto

from controller.file_manager.ExportCreator import ExportCreator
from controller.file_manager.FileManagerInterface import FileManagerInterface
from controller.file_manager.FileOpener import FileOpener
from controller.file_manager.FileSaver import FileSaver
from controller.init_v_controll_logic.ExportOptions import ExportOptions
from model.Configuration import Configuration
from model.Session import Session


class FileManager(FileManagerInterface):
    def load(self, source_path: str, option: str) -> Configuration or Session or cyto.Cytoscape:
        """
        implements the load as defined in the interface
        :param source_path: string of the path to the data
        :param option: string (`c` for Configuration, `s` for session)
        """
        # TODO test
        opener = FileOpener()
        return opener.load(source_path, option)

    def save(self, output_path: str, input: Configuration or Session, *args):
        """
         implements the save as defined in the interface
         :param output_path: string of the output path (path || name).
         :param input: Session | Configuration
        """
        # TODO test
        saver = FileSaver()
        saver.save(output_path, input, *args)

    def export(self, output_path: str, session: Session, options: ExportOptions):
        """
        implements the export as defined in the interface.
        :param output_path: string to the output
        :param session: Session object containing the data
        :param options: ExportOptions object containing the parameters for the export.
        """
        # TODO implement
        ec = ExportCreator()
        ec.export(output_path, session, options)

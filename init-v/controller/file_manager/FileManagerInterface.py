from model.Session import *
from controller.init_v_controll_logic.ExportOptions import *
import dash_cytoscape as cyto


class FileManagerInterface:

    def load(self, source_path: str, option: str) -> Session or Configuration or cyto.Cytoscape:
        """
        interface method for loading a session, configuration or cyto.cytoscape back from the disk
        :param source_path: string of the source path.
        :param option: string, used to differentiate between loading a configuration and a Session.
                        `c` for Configuration, `s` for Session, 't' for cyto.cytoscape
        """
        pass

    def save(self, output_path: str, input: Configuration or Session, *args):
        """
        interface method for saving a Session or Configuration to the disk. If no
        :param input: Configuration or Session, input to be saved
        :param output_path: string ,containing the full path (path to directory || name).
        """
        pass

    def export(self, output_path: str, session: Session, options: ExportOptions):
        """
        interface method for Exporting the graphs to the disk.
        :param session: Session, to be exported
        :param output_path: string ,containing the full path (path to directory || name).
        :param options: ExportOptions, options to specify export behaviour
        """
        pass

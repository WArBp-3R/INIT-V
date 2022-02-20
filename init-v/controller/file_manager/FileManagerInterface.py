from model.Configuration import *
from model.Session import *
from controller.init_v_controll_logic.ExportOptions import *

class FileManagerInterface:
    """
    interface method for loading a configuration back from the disk.

    :param source_path: string of the source path.
    :option: string, used to differentiate between loading a configuration and a Session. `c` for Configuration, `s` for Session
    """
    def load(self, source_path: str, option: str) -> Configuration:
        pass

    """
    interface method for loading a configuration back from the disk.

    :param source_path: string of the source path.
    :param option: string, used to differentiate between loading a configuration and a Session. `c` for Configuration, `s` for Session
    """
    def load(self, source_path: str, option: str) -> Session:
        pass

    """
    interface method for saving a Session to the disk.

    :param output_path: string ,containing the full path (path to directory || name).
    """
    def save(self, output_path: str, session: Session):
        pass

    """
    interface method for saving a Configuration to the disk. If no 

    :param output_path: string ,containing the full path (path to directory || name).
    """
    def save(self, output_path: str, config: Configuration):
        pass

    """
    interface method for Exporting the graphs to the disk.

    :param output_path: string ,containing the full path (path to directory || name).
    """
    def export(self, output_path: str, session: Session, options: ExportOptions):

        pass

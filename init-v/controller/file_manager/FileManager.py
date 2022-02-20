

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
import dash_cytoscape as cyto



class FileManager(FileManagerInterface):
    """
    implements the load as defined in the interface

    :param source_path: string of the path to the data
    :param option: string (`c` for Configuration, `s` for session)
    """
    def load(self, source_path: str, option: str) -> Configuration or Session or cyto.Cytoscape:
        #TODO test
        opener = FileOpener()
        return opener.load(source_path, option)
        pass


    """
     implements the save as defined in the interface 

     :param output_path: string of the output path (path || name).
     :param input: Session | Configuration
     """

    def save(self, output_path: str, input: Configuration or Session, *args):
        #TODO test
        saver = FileSaver()
        saver.save(output_path, input, args[0])
        pass

    """
    implements the export as defined in the interface.
    
    :param output_path: string to the output
    :param session: Session object containing the data
    :param options: ExportOptions object containing the parameters for the export.
    """
    def export(self, output_path: str, session: Session, options: ExportOptions):
        #TODO implement
        ExportCreator.export(output_path, session, options)
        pass



def main():
    print("hi")
    f = FileManager()
    acon = AutoencoderConfiguration(2, [2, 2], "foo", 5, "bar")
    con = Configuration(True, True, 5, "tooo", "L1", acon)
    run_1 = RunResult(10, con, None, None)
    run_2 = RunResult(34, con, None, None)
    topology = NetworkTopology(None, [12, 24, 12])
    list = [run_2, run_1]
    protocols :set[str] = set()
    protocols.add("TCP")
    protocols.add("UDP")
    protocols.add("Profinet")
    protocols.add("Aloha")
    protocols.add("Arp")
    protocols.add("foo")
    protocols.add("bar")
    # session = Session("C:/Users/Mark/Desktop/Test/Material/example.pcapng", protocols, list, con, topology, None)
    # f.save("C:/Users/Mark/Desktop/Test/saves", session)
    # config = f.load("C:/Users/Mark/Desktop/Test/active_configuration.csv", "c")
    # new_session = f.load("C:/Users/Mark/Desktop/Test/saves", "s")

    f.save("C:/Users/Mark/Desktop/Test/saves/config_test_saver", con)

    pass



if __name__ == "__main__":
    main()
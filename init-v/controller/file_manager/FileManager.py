

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

    # old, with method overloading
    # def saveSession(self, output_path: str, session: Session):
    #     saver = FileSaver()
    #     saver.saveSession(output_path, session)
    #     pass

    def save(self, output_path: str, input: Configuration or Session):
        #TODO test
        saver = FileSaver()
        saver.save(output_path, input)


        pass

    def export(self, output_path: str, session: Session, options: ExportOptions):
        #TODO implement
        ExportCreator.export(output_path, session, options)
        pass



def main():
    print("hi")
    f = FileManager()
    acon = AutoencoderConfiguration(2, [2, 2], "foo", 5, "bar")
    con = Configuration(True, True, 5, "tooo", acon)
    run_1 = RunResult(10, con, None, None, None)
    run_2 = RunResult(34, con, None, None, None)
    topology = NetworkTopology(None, [12, 24, 12])
    list = [run_2, run_1]
    session = Session("C:\\Users\\Mark\\Desktop\\Test\\Material\\PCAP.txt", None, list, con, topology)
    f.save("C:\\Users\\Mark\\Desktop\\Test", session)
    f.save("C:\\Users\\Mark\\Desktop\\Test\\config_test_saver", con)
    config = f.load("C:\\Users\\Mark\\Desktop\\Test\\active_configuration.csv", "c")
    session = f.load("C:\\Users\\Mark\\Desktop\\Test", "s")


    pass



if __name__ == "__main__":
    main()
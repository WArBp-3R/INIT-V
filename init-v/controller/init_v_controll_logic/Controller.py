import os
import pathlib

from controller.file_manager.FileManager import FileManager
from controller.init_v_controll_logic.ControllerInterface import ControllerInterface
from controller.init_v_controll_logic.ExportOptions import ExportOptions
from controller.init_v_controll_logic.Settings import Settings

from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from model.Session import Session
from model.RunResult import RunResult
from model.network.NetworkTopology import NetworkTopology

from model.Configuration import Configuration
from controller.init_v_controll_logic import ExportOptions
from model.Session import Session
from controller.init_v_controll_logic.Settings import Settings
from datetime import datetime
from keras.callbacks import History
from model.network.NetworkTopology import NetworkTopology
from model.IStatistic import IStatistic


class Controller (ControllerInterface):
    WORKSPACE_PATH: str
    # session: Session
    # settings: Settings

    def __init__(self, session: Session, settings: Settings):
        self.session = session
        self.settings = settings
        self.fileManager = FileManager()
        os.chdir('../../')
        path = os.getcwd()
        path += "\\out"

        #generates all the folders needed if missing
        try:
            self.settings_path = path + "\\DEFAULT_SETTINGS"
            os.makedirs(path + "\\DEFAULT_SETTINGS")

        except OSError:
            #TODO add error handling
            pass
        try:
            self.configuration_path = path + "\\Configurations"
            os.makedirs(path + "\\Configurations")
        except OSError:
            #TODO add error handling
            pass
        try:
            self.saves_path = path + "\\Saves"
            os.makedirs(path + "\\Saves")
        except OSError:
            #TODO add error handling
            pass


    def startup(self):
        #TODO implement
        pass

    def update_topology(self):
        #TODO implement
        pass

    def create_run(self, pca_performance: list[(float, float)], pca_result: list[(float, float, str)],
                   autoencoder_performance: list[History], autoencoder_result: list[(float, float, str)],
                   topology: list[NetworkTopology], timestamp: list[datetime], stats: list[IStatistic],
                   config: list[Configuration]):
        #TODO implement
        #create run, save in model and update the given attributes, which are all!! lists.
        #if an object is not a list just do varX = [<object_not_being_a_list>]
        pass

    #def update_config(self, config: Configuration):
    #    #TODO implement
    #    pass

    def create_new_session(self, session: Session):
        # TODO implement
        pass

    def compare_runs(self, pos: list[int], pca_results: list[list[(float, float, str)]],
                     pca_performances: list[list[(float, float)]], autoencoder_performances: list[History],
                     autoencoder_results: list[list[(float, float, str)]],
                     timestamps: list[datetime], stats: list[list[datetime]], topology: list[NetworkTopology],
                     config: list[Configuration]):
        #TODO implement
        pass

    def load_session(self, source_path: str, pca_performance: list[(float, float)],
                     pca_result: list[(float, float, str)], autoencoder_performance: list[History],
                     autoencoder_result: list[(float, float, str)], topology: list[NetworkTopology],
                     timestamp: list[datetime], stats: list[IStatistic], config: list[Configuration]):
        #TODO implement
        if os.path.isdir(source_path):
            new_session = self.fileManager.load(source_path, "s")
        elif True:
            new_session :Session = self.fileManager.load(self.saves_path + "\\" +  source_path, "s")
        #load session
        #save in session variable
        #update values, which are, again, all!! lists.
        pass

    def load_config(self, source_path: str) -> Configuration:
        #TODO implement
        if os.path.isfile(source_path):
            config = self.fileManager.load(source_path, "c")
            self.session.active_config = config
        elif True:
            config = self.fileManager.load(self.configuration_path + "\\" + source_path, "c")
            self.session.active_config = config

        #load config
        #write to model
        #return config
        pass

    def save_session(self, output_path: str, config: Configuration):
        #TODO implement
        path = pathlib.Path(output_path)
        path = path.parent
        if str(path) != ".":
            self.fileManager.save(output_path, self.session)
        elif True:
            self.fileManager.save(self.saves_path + "\\" + output_path , self.session)
        #config is the active Configuration
        pass

    def save_config(self, output_path: str, config: Configuration):
        #TODO implement
        path = pathlib.Path(output_path)
        path = path.parent
        if str(path) != ".":
            self.fileManager.save(output_path, self.session.active_config)
        elif True:
            self.fileManager.save(self.configuration_path + "\\" + output_path, self.session.active_config)


        pass

    def export(self, output_path: str, options: ExportOptions):
        #TODO implement
        pass

    def get_run_list(self) -> list[datetime]:
        #TODO implement
        pass
def main():

    # f = FileManager()
    acon = AutoencoderConfiguration(2, [2, 2], "foo", 5, "bar")
    con = Configuration(True, True, 5, "tooo", acon)
    run_1 = RunResult(10, con, None, None, None)
    run_2 = RunResult(34, con, None, None, None)
    topology = NetworkTopology(None, [12, 24, 12])
    list = [run_2, run_1]
    session = Session("C:\\Users\\Mark\\Desktop\\Test\\Material\\PCAP.txt", None, list, con, topology, None)
    # f.save("C:\\Users\\Mark\\Desktop\\Test", session)
    # f.save("C:\\Users\\Mark\\Desktop\\Test\\config_test_saver", con)
    # config = f.load("C:\\Users\\Mark\\Desktop\\Test\\active_configuration.csv", "c")
    # session = f.load("C:\\Users\\Mark\\Desktop\\Test", "s")

    controller = Controller(session, None)

    controller.save_config("Test")
    controller.save_config("C:\\Users\\Mark\\PycharmProjects\\init-v\\init-v\\out\\Configurations\\Hallo.csv")
    controller.save_config("C:\\test.csv")
    controller.load_config("C:\\Users\\Mark\\PycharmProjects\\init-v\\init-v\\out\\Configurations\\Hallo.csv")
    controller.load_config("Test")
    controller.save_session("Test")
    controller.save_session("C:\\Users\\Mark\\PycharmProjects\\init-v\\init-v\\out\\Saves\\Test Run")


    pass



if __name__ == "__main__":
    main()
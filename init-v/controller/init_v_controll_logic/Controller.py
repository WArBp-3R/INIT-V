import os
import pathlib
from datetime import datetime
from keras.callbacks import History

from controller.file_manager.FileManager import FileManager
from controller.init_v_controll_logic.ControllerInterface import ControllerInterface
from controller.init_v_controll_logic.ExportOptions import ExportOptions
from controller.init_v_controll_logic.Settings import Settings
from controller.init_v_controll_logic.Calculator import Calculator

from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from model.Session import Session
from model.RunResult import RunResult
from model.network.NetworkTopology import NetworkTopology
from model.IStatistic import IStatistic

from view.ViewAdapter import ViewAdapter


class Controller(ControllerInterface):
    WORKSPACE_PATH: str

    def __init__(self, session: Session, settings: Settings):
        if session is None:
            self.calculator = None
        else:
            self.calculator = Calculator(session.PCAP_PATH)
        self.session = session
        self.settings = settings
        self.fileManager = FileManager()
        self.view = ViewAdapter(self)

        # goes to the right directory (2 up)
        os.chdir('../../')
        path = os.getcwd()

        # sets the path to a new directory "out" to separate the data and code better
        path += "\\out"

        # generates all the folders needed if missing
        try:
            self.settings_path = path + "\\DEFAULT_SETTINGS"
            os.makedirs(path + "\\DEFAULT_SETTINGS")

        except OSError:
            # TODO add error handling
            pass

        try:
            self.configuration_path = path + "\\Configurations"
            os.makedirs(path + "\\Configurations")
        except OSError:
            # TODO add error handling
            pass

        try:
            self.saves_path = path + "\\Saves"
            os.makedirs(path + "\\Saves")
        except OSError:
            # TODO add error handling
            pass

    def startup(self):
        # TODO implement

        pass

    def update_topology(self):
        # TODO implement
        pass

    def open(self, path: str, **kwargs):
        # checks which file type or directory will be processed and calls the according method
        if path.endswith(".csv"):
            self.load_config(path)
        elif os.path.isdir(path):
            self.load_session(path, kwargs["pcap_performance"], kwargs["pca_result"], kwargs["autoencoder_performance"],
                              kwargs["autoencoder_result"], kwargs["topology"], kwargs["timestamp"], kwargs["stats"],
                              kwargs["config"])
        elif path.endswith(".pcapng"):
            self.create_new_session(path)

    def create_run(self, pca_performance: list[(float, float)], pca_result: list[(float, float, str)],
                   autoencoder_performance: list[History], autoencoder_result: list[(float, float, str)],
                   topology: list[NetworkTopology], timestamp: list[datetime], stats: list[IStatistic],
                   config: list[Configuration]):
        # TODO test

        run = self.calculator.calculate_run(config[0])
        self.session.run_results.append(run)
        self.session.active_config = config[0]

        pca_performance = self.session.run_results[-1].analysis.get_pca()
        pca_result = self.session.run_results[-1].result.pca_result
        autoencoder_performance = [self.session.run_results[-1].analysis.get_autoencoder()]
        autoencoder_result = self.session.run_results[-1].result.autoencoder_result
        topology = [self.session.topology]
        timestamp = [self.session.run_results[-1].timestamp]
        stats = self.session.run_results[-1].statistics.stats
        config = [self.session.active_config]

        # create run, save in model and update the given attributes, which are all!! lists.

        pass

    # def update_config(self, config: Configuration):
    #    #TODO implement
    #    pass

    def create_new_session(self, PCAP_Path: str):
        # TODO test
        self.calculator = Calculator(PCAP_Path)
        topology = self.calculator.calculate_topology()
        config = self.settings.DEFAULT_CONFIGURATION
        protocols = self.calculator.protocols
        new_session = Session(PCAP_Path, protocols, [], config, topology, None)

        self.session = new_session
        pass

    def compare_runs(self, pos: list[int], pca_results: list[list[(float, float, str)]],
                     pca_performances: list[list[(float, float)]], autoencoder_performances: list[History],
                     autoencoder_results: list[list[(float, float, str)]],
                     timestamps: list[datetime], stats: list[list[datetime]], topology: list[NetworkTopology],
                     config: list[Configuration]):

        # TODO test
        for i in pos:
            pca_results.append(self.session.run_results[i].result.pca_result)
            pca_performances.append(self.session.run_results[i].analysis.get_pca())
            autoencoder_performances.append(self.session.run_results[i].analysis.get_autoencoder())
            autoencoder_results.append(self.session.run_results[i].result.autoencoder_result)
            timestamps.append(self.session.run_results[i].timestamp)
            stats.append(self.session.run_results[i].statistics.stats)
            config.append(self.session.run_results[i].config)

        topology = [self.session.topology]

        pass

    def load_session(self, source_path: str, pca_performance: list[(float, float)],
                     pca_result: list[(float, float, str)], autoencoder_performance: list[History],
                     autoencoder_result: list[(float, float, str)], topology: list[NetworkTopology],
                     timestamp: list[datetime], stats: list[IStatistic], config: list[Configuration]):
        # TODO implement starting new instance

        if os.path.isdir(source_path):
            self.session = self.fileManager.load(source_path, "s")
        elif True:
            self.session = self.fileManager.load(self.saves_path + "\\" + source_path, "s")

        pca_performance = self.session.run_results[-1].analysis.get_pca()
        pca_result = self.session.run_results[-1].result.pca_result
        autoencoder_performance = [self.session.run_results[-1].analysis.get_autoencoder()]
        autoencoder_result = self.session.run_results[-1].result.autoencoder_result
        topology = [self.session.topology]
        timestamp = [self.session.run_results[-1].timestamp]
        stats = self.session.run_results[-1].statistics.stats
        config = [self.session.active_config]

        # save in session variable
        pass

    def load_config(self, source_path: str) -> Configuration:
        # TODO test

        if os.path.isfile(source_path):
            config = self.fileManager.load(source_path, "c")
            self.session.active_config = config
            return config
        elif True:
            config = self.fileManager.load(self.configuration_path + "\\" + source_path, "c")
            self.session.active_config = config
            return config

        # load config
        # write to model
        # return config

        pass

    def save_session(self, output_path: str, config: Configuration):
        # TODO test
        path = pathlib.Path(output_path)
        path = path.parent
        if str(path) != ".":
            self.fileManager.save(output_path, self.session)
        elif True:
            self.fileManager.save(self.saves_path + "\\" + output_path, self.session)
        pass

    def save_config(self, output_path: str, config: Configuration):
        # TODO test
        path = pathlib.Path(output_path)
        path = path.parent
        if str(path) != ".":
            self.fileManager.save(output_path, self.session.active_config)
        elif True:
            self.fileManager.save(self.configuration_path + "\\" + output_path, self.session.active_config)
        pass

    def export(self, output_path: str, options: ExportOptions):
        # TODO implement
        pass

    def get_run_list(self) -> list[datetime]:
        # TODO implement
        pass


def main():
    # f = FileManager()
    acon = AutoencoderConfiguration(2, [2, 2], "foo", 5, "bar")
    con = Configuration(True, True, 5, "tooo", acon)
    run_1 = RunResult(10, con, None, None)
    run_2 = RunResult(34, con, None, None)
    topology = NetworkTopology(None, [12, 24, 12])
    list = [run_2, run_1]
    session = Session("D:\\workspace\\PSE\\init-v\\init-v\\backend\\example.pcapng", None, list, con, topology, None)
    # f.save("C:\\Users\\Mark\\Desktop\\Test", session)
    # f.save("C:\\Users\\Mark\\Desktop\\Test\\config_test_saver", con)
    # config = f.load("C:\\Users\\Mark\\Desktop\\Test\\active_configuration.csv", "c")
    # session = f.load("C:\\Users\\Mark\\Desktop\\Test", "s")

    controller = Controller(session, None)
    print("Nach instanzierung")
    controller.create_new_session("D:\\workspace\\PSE\\init-v\\init-v\\backend\\example.pcapng")

    # controller.save_config("Test")
    # controller.save_config("C:\\Users\\Mark\\PycharmProjects\\init-v\\init-v\\out\\Configurations\\Hallo.csv")
    # controller.save_config("C:\\test.csv")
    # controller.load_config("C:\\Users\\Mark\\PycharmProjects\\init-v\\init-v\\out\\Configurations\\Hallo.csv")
    # controller.load_config("Test")
    # controller.save_session("Test")
    # controller.save_session("C:\\Users\\Mark\\PycharmProjects\\init-v\\init-v\\out\\Saves\\Test Run")

    pass


if __name__ == "__main__":
    main()

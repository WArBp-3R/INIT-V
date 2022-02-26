import os
import pathlib
from datetime import datetime

import dash_cytoscape
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
from model.Statistics import Statistics
from model.network.NetworkTopology import NetworkTopology
from model.IStatistic import IStatistic

from view.ViewAdapter import ViewAdapter

class Controller(ControllerInterface):
    WORKSPACE_PATH: str

    """
    Constructor of the Controller class. 
    sets up all directories and the default settings.
    
    :param session: Session object
    """
    def __init__(self, session: Session, settings: Settings):
        if session is None:
            self.calculator = None
        else:
            self.calculator = Calculator(session.PCAP_PATH)
        self.session = session
        self.fileManager = FileManager()

        # goes to the right directory (2 up)
        print(os.getcwd())
        path = os.getcwd().removesuffix( os.sep + "controller" + os.sep + "init_v_controll_logic")

        # sets the path to a new directory "out" to separate the data and code better
        path +=  os.sep + "out"
        self.settings = Settings(path)

        # generates all the folders needed if missing
        try:
            self.settings_path = path + os.sep + "DEFAULT_SETTINGS"
            os.makedirs(path + os.sep + "DEFAULT_SETTINGS")

        except OSError:
            # TODO add error handling
            pass

        try:
            self.configuration_path = path + os.sep + "Configurations"
            os.makedirs(path + os.sep + "Configurations")
        except OSError:
            # TODO add error handling
            pass

        try:
            self.saves_path = path + os.sep + "Saves"
            os.makedirs(path + os.sep + "Saves")
        except OSError:
            # TODO add error handling
            pass

        self.view = ViewAdapter(self)

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

    def create_run(self, config: Configuration) -> int:
        # TODO test

        run = self.calculator.calculate_run(config)
        self.session.run_results.append(run)
        self.session.active_config = config
        return -1

    def update_config(self, config: Configuration):
        self.session.active_config = config

    def get_active_config(self) -> Configuration:
        return self.session.active_config

    def get_default_config(self) -> Configuration:
        # TODO - check if behavior is actually correct
        return self.settings.DEFAULT_CONFIGURATION

    def set_default_config(self, config: Configuration):
        self.settings.DEFAULT_CONFIGURATION = config

    def create_new_session(self, PCAP_Path: str):
        # TODO test
        self.calculator = Calculator(PCAP_Path)
        topology = self.calculator.calculate_topology()
        config = None if self.settings is None else self.settings.DEFAULT_CONFIGURATION
        protocols = self.calculator.protocols
        highest_protocols = self.calculator.highest_protocols
        new_session = Session(PCAP_Path, protocols, highest_protocols, [], config, topology, self.calculator.statistics)

        self.session = new_session
        pass

    def compare_runs(self, pos: list[int]) -> list[RunResult]:
        # TODO test
        rlist = []
        for i in pos:
            rlist.append(self.session.run_results[i])
        return rlist

    def load_session(self, source_path: str) -> Session:
        # TODO implement starting new instance

        if os.path.isdir(source_path):
            self.session = self.fileManager.load(source_path, "s")
        elif True:
            self.session = self.fileManager.load(self.saves_path + os.sep + source_path, "s")



        if len(self.session.run_results) != 0:
            pca_performance = self.session.run_results[-1].analysis.get_pca()
            pca_result = self.session.run_results[-1].result.pca_result
            autoencoder_performance = [self.session.run_results[-1].analysis.get_autoencoder()]
            autoencoder_result = self.session.run_results[-1].result.autoencoder_result
            timestamp = [self.session.run_results[-1].timestamp]
            stats = self.session.run_results[-1].statistics.stats

        topology = [self.session.topology]
        config = [self.session.active_config]

        # potentially less redundant version that hopefully works
        # last_run = self.session.run_results[-1]
        #
        # pca_performance = last_run.analysis.get_pca()
        # pca_result = last_run.result.pca_result
        # autoencoder_performance = [last_run.analysis.get_autoencoder()]
        # autoencoder_result = last_run.result.autoencoder_result
        # topology = [self.session.topology]
        # timestamp = [last_run.timestamp]
        # stats = last_run.statistics.stats
        # config = [self.session.active_config]

        # save in session variable
        return self.session

    def load_config(self, source_path: str) -> Configuration:
        # TODO test

        if os.path.isfile(source_path):
            config = self.fileManager.load(source_path, "c")
            self.session.active_config = config
            return config
        elif True:
            config = self.fileManager.load(self.configuration_path + os.sep + source_path, "c")
            self.session.active_config = config
            return config

        # load config
        # write to model
        # return config

        pass

    def load_topology_graph(self, source_path: str) -> dash_cytoscape.Cytoscape:
        t_g: dash_cytoscape.Cytoscape
        if os.path.isdir(source_path):
            t_g = self.fileManager.load(source_path, "t")
        elif True:
            t_g = self.fileManager.load(self.saves_path + os.sep + source_path, "t")
        return t_g

    def save_session(self, output_path: str, config: Configuration, topology_graph: dash_cytoscape.Cytoscape):
        # TODO config not needed if held consistently updated
        # TODO test
        if config is None:
            config = self.session.active_config

        if output_path is None:
            suffix =  os.sep + self.session.PCAP_PATH.split( os.sep )[-1]
            output_path = self.session.PCAP_PATH.removesuffix(suffix)

        path = pathlib.Path(output_path)
        path = path.parent
        if str(path) != ".":
            self.fileManager.save(output_path, self.session, topology_graph)
            # suffix =  os.sep  + self.session.PCAP_PATH.split( os.sep )[-1]
            self.session.PCAP_PATH = output_path + os.sep + "PCAP.pcapng"
        elif True:
            self.fileManager.save(self.saves_path +  os.sep + output_path, self.session, topology_graph)
            # suffix =  os.sep + self.session.PCAP_PATH.split( os.sep )[-1]
            self.session.PCAP_PATH = self.saves_path + os.sep + output_path + os.sep + "PCAP.pcapng"
        pass

    def save_config(self, output_path: str, config: Configuration):
        # TODO test
        path = pathlib.Path(output_path)
        path = path.parent
        if str(path) != ".":
            self.fileManager.save(output_path, self.session.active_config)
        elif True:
            self.fileManager.save(self.configuration_path +  os.sep + output_path, self.session.active_config)
        pass

    def export(self, output_path: str, options: ExportOptions):
        # TODO implement
        pass

    def get_run_list(self) -> list[RunResult]:
        # TODO implement
        return self.session.run_results

    def get_network_topology(self) -> NetworkTopology:
        return self.session.topology

    def get_highest_protocols(self) -> set[str]:
        return self.session.highest_protocols

    def get_statistics(self) -> Statistics:
        return self.session.statistics


def main():
    # f = FileManager()
    acon = AutoencoderConfiguration(2, [2, 2], "foo", 5, "bar")
    con = Configuration(True, True, 5, True, "tooo", acon)
    run_1 = RunResult(10, con, None, None)
    run_2 = RunResult(34, con, None, None)
    topology = NetworkTopology(None, [12, 24, 12])
    list = [run_2, run_1]
    session = Session("D:/workspace/PSE/init-v/code/backend/example.pcapng", None, list, con, topology, None, None)
    # session2 = Session("D:/workspace/PSE/init-v/code/backend/example.pcapng", None, list, con, topology, None, None)
    # f.save("C:\\Users\\Mark\\Desktop\\Test", session)
    # f.save("C:\\Users\\Mark\\Desktop\\Test\\config_test_saver", con)
    # config = f.load("C:\\Users\\Mark\\Desktop\\Test\\active_configuration.csv", "c")
    # session = f.load("C:\\Users\\Mark\\Desktop\\Test", "s")

    controller = Controller(session, None)

    controller.create_new_session("D:/workspace/PSE/init-v/code/backend/example.pcapng")

    # controller.save_config("Test")
    # controller.save_config("C:\\Users\\Mark\\PycharmProjects\\init-v\\init-v\\out\\Configurations\\Hallo.csv")
    # controller.save_config("C:\\test.csv")
    # controller.load_config("C:\\Users\\Mark\\PycharmProjects\\init-v\\init-v\\out\\Configurations\\Hallo.csv")
    # controller.load_config("Test")
    # controller.save_session("Test")
    # controller.save_session("C:\\Users\\Mark\\PycharmProjects\\init-v\\init-v\\out\\Saves\\Test Run")

    controller.view.start_view()
    pass


if __name__ == "__main__":
    main()

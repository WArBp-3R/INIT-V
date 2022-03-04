import os
import pathlib

import dash_cytoscape

from controller.file_manager.FileManager import FileManager
from controller.init_v_controll_logic.ControllerInterface import ControllerInterface
from controller.init_v_controll_logic.ExportOptions import ExportOptions
from controller.init_v_controll_logic.Settings import Settings
from controller.init_v_controll_logic.Calculator import Calculator

from model.Configuration import Configuration
from model.Session import Session
from model.RunResult import RunResult
from model.Statistics import Statistics
from model.network.NetworkTopology import NetworkTopology

from view.ViewAdapter import ViewAdapter


class Controller(ControllerInterface):
    WORKSPACE_PATH: str

    def __init__(self, session: Session, settings: Settings):
        """
        Constructor of the Controller class.
        sets up all directories and the default settings.

        :param session: Session object
        """
        self.calculator = Calculator(session.PCAP_PATH) if session else None
        self.session = session
        self.fileManager = FileManager()

        # goes to the right directory (2 up)
        print(os.getcwd())
        path = os.getcwd().removesuffix(os.sep + "controller" + os.sep + "init_v_controll_logic")

        # sets the path to a new directory "out" to separate the data and code better
        path += os.sep + "out"
        self.settings = Settings(path)

        # generates all the folders needed if missing
        self._generate_directories(path)

        self.view = ViewAdapter(self)

    def _generate_directories(self, path):
        # directories = [path + os.sep + d for d in ["DEFAULT_SETTINGS", "Configurations", "Saves"]]
        try:
            self.settings_path = path + os.sep + "DEFAULT_SETTINGS"
            os.makedirs(self.settings_path)
        except OSError:
            # TODO add error handling
            pass

        try:
            self.configuration_path = path + os.sep + "Configurations"
            os.makedirs(self.configuration_path)
        except OSError:
            # TODO add error handling
            pass

        try:
            self.saves_path = path + os.sep + "Saves"
            os.makedirs(self.saves_path)
        except OSError:
            # TODO add error handling
            pass

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
        return self.settings.DEFAULT_CONFIGURATION

    def set_default_config(self, config: Configuration):
        self.settings.set_default_config(config)

    def get_run_list(self) -> list[RunResult]:
        return self.session.run_results

    def compare_runs(self, pos: list[int]) -> list[RunResult]:
        # TODO test
        rlist = []
        for i in pos:
            rlist.append(self.session.run_results[i])
        return rlist

    def get_network_topology(self) -> NetworkTopology:
        return self.session.topology

    def get_highest_protocols(self) -> set[str]:
        return self.session.highest_protocols

    def get_statistics(self) -> Statistics:
        return self.session.statistics

    def create_new_session(self, pcap_path: str):
        # TODO test
        self.calculator = Calculator(pcap_path)
        topology = self.calculator.calculate_topology()
        config = None if self.settings is None else self.settings.DEFAULT_CONFIGURATION
        protocols = self.calculator.protocols
        highest_protocols = self.calculator.highest_protocols
        new_session = Session(pcap_path, protocols, highest_protocols, [], config, topology, self.calculator.statistics)

        self.session = new_session

    def load_config(self, source_path: str) -> Configuration:
        # TODO test
        actual_path = source_path if os.path.isfile(source_path) else self.configuration_path + os.sep + source_path
        config = self.fileManager.load(actual_path, "c")
        self.session.active_config = config
        return config

    def save_config(self, output_path: str, config: Configuration):
        # TODO test
        path = pathlib.Path(output_path)
        path = path.parent
        actual_path = output_path if str(path) != "." else self.configuration_path + os.sep + output_path
        self.fileManager.save(actual_path, self.session.active_config)

    def load_session(self, source_path: str) -> Session:
        if source_path == "#prev":
            source_path = pathlib.Path(self.saves_path, "previous_session.path").read_text()
        actual_path = source_path if os.path.isdir(source_path) else self.saves_path + os.sep + source_path
        self.session = self.fileManager.load(actual_path, "s")
        print("loaded session at path: {}".format(source_path))
        pathlib.Path(self.saves_path, "previous_session.path").write_text(source_path)
        return self.session

    def save_session(self, output_path: str, topology_graph: dash_cytoscape.Cytoscape):
        # TODO test
        if output_path is None:
            filename_without_extension = self.session.PCAP_PATH.split(os.sep)[-1].split(".")[0]
            output_path = self.saves_path + os.sep + filename_without_extension

        path = pathlib.Path(output_path)
        path = path.parent
        self.fileManager.save(output_path, self.session, topology_graph)
        self.session.PCAP_PATH = output_path + os.sep + "PCAP.pcapng"

    def get_session(self):
        return self.session

    def load_topology_graph(self, source_path: str) -> dash_cytoscape.Cytoscape:
        t_g: dash_cytoscape.Cytoscape
        actual_path = source_path if os.path.isdir(source_path) else self.saves_path + os.sep + source_path
        t_g = self.fileManager.load(actual_path, "t")
        return t_g

    def export(self, output_path: str, options: ExportOptions):
        # TODO implement
        pass


def main():
    print("INIT-V start:")
    controller = Controller(None, None)
    controller.view.start_view()


if __name__ == "__main__":
    main()

import os
import pathlib
from pathlib import Path


import dash_cytoscape

from controller.file_manager.FileManager import FileManager
from controller.init_v_controll_logic.ControllerInterface import ControllerInterface
from controller.init_v_controll_logic.ExportOptions import ExportOptions
from controller.init_v_controll_logic.Settings import Settings
from controller.init_v_controll_logic.Calculator import Calculator

from model.Configuration import Configuration
from model.Configuration import AutoencoderConfiguration
from model.Session import Session
from model.RunResult import RunResult
from model.Statistics import Statistics
from model.network.NetworkTopology import NetworkTopology

from view.ViewAdapter import ViewAdapter

_DEFAULT_CONFIGURATION = Configuration(True, True, 150, "Length", "None", AutoencoderConfiguration(
    4, [256, 64, 32, 8], "MSE", 100, "adam"))


class Controller(ControllerInterface):

    def __init__(self, session: Session, settings: Settings):
        """
        Constructor of the Controller class.
        sets up all directories and the default settings.

        :param session: Session object
        """
        self.calculator = Calculator(session.pcap_path) if session else None
        self.session = session
        self.fileManager = FileManager()

        # Define default used paths.
        self.workspace_path = f"{Path.home()}{os.sep}INIT-V"
        self.settings_path = f"{self.workspace_path}{os.sep}DEFAULT_SETTINGS"
        self.configuration_path = f"{self.workspace_path}{os.sep}Configurations"
        self.saves_path = f"{self.workspace_path}{os.sep}Saves"

        # generates all the folders needed if missing
        self._generate_directories()
        self.settings = Settings(self.workspace_path)

        self.view = ViewAdapter(self)

    def _generate_directories(self):
        try:
            workspace_exists = False
            if not os.path.isdir(self.workspace_path):
                os.mkdir(self.workspace_path)
            else:
                workspace_exists = True
            if not workspace_exists or not os.path.isdir(self.settings_path):
                os.mkdir(self.settings_path)
            if not workspace_exists or not os.path.isfile(f"{self.settings_path}{os.sep}"
                                                          "DEFAULT_CONFIGURATION.csv"):
                self.fileManager.save(f"{self.settings_path}{os.sep}DEFAULT_CONFIGURATION.csv",
                                      _DEFAULT_CONFIGURATION)
            if not workspace_exists or not os.path.isdir(self.configuration_path):
                os.mkdir(self.configuration_path)
            if not workspace_exists or not os.path.isdir(self.saves_path):
                os.mkdir(self.saves_path)
        except OSError:
            print("Failed to initialize workspace, exiting...")
            exit(-1)

    def create_run(self, config: Configuration) -> int:
        # TODO test
        run = self.calculator.calculate_run(config)
        self.session.run_results.append(run)
        self.session.active_config = config
        return -1

    def compare_runs(self, pos: list[int]) -> list[RunResult]:
        # TODO test
        rlist = []
        for i in pos:
            rlist.append(self.session.run_results[i])
        return rlist

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
        self.calculator = Calculator(self.session.PCAP_PATH)
        print("loaded session at path: {}".format(source_path))
        pathlib.Path(self.saves_path, "previous_session.path").write_text(source_path)
        return self.session

    def save_session(self, output_path: str, topology_graph: dash_cytoscape.Cytoscape):
        if output_path is None:
            output_path = self.saves_path + os.sep + os.path.basename(self.session.pcap_path)
        self.fileManager.save(output_path, self.session, topology_graph)
        self.session.pcap_path = output_path + os.sep + "PCAP.pcapng"

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


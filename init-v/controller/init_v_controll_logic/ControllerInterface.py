from model.RunResult import RunResult

from model.Configuration import Configuration
from controller.init_v_controll_logic import ExportOptions
from model.Session import Session

from model.Statistics import Statistics
from model.network.NetworkTopology import NetworkTopology
import dash_cytoscape as cyto


class ControllerInterface:
    def create_run(self, config: Configuration) -> int:
        # TODO comment
        pass

    def update_config(self, config: Configuration):
        # TODO comment
        pass

    def get_active_config(self) -> Configuration:
        # TODO comment
        pass

    def get_default_config(self) -> Configuration:
        # TODO comment
        pass

    def set_default_config(self, config: Configuration):
        # TODO comment
        pass

    def get_run_list(self) -> list[RunResult]:
        # TODO comment
        pass

    def compare_runs(self, pos: list[int]) -> list[RunResult]:
        # TODO comment
        pass

    def get_network_topology(self) -> NetworkTopology:
        # TODO comment
        pass

    def get_highest_protocols(self) -> set[str]:
        # TODO comment
        pass

    def get_statistics(self) -> Statistics:
        # TODO comment
        pass

    def create_new_session(self, pcap_path: str):
        # TODO comment
        pass

    def load_config(self, source_path: str) -> Configuration:
        # TODO comment
        pass

    def save_config(self, output_path: str, config: Configuration):
        # TODO comment
        pass

    def load_session(self, source_path: str) -> Session:
        # TODO comment
        pass

    def save_session(self, output_path: str, topology_graph: cyto.Cytoscape):
        # TODO comment
        pass

    def get_session(self):
        # TODO comment
        pass

    def export(self, output_path: str, options: ExportOptions):
        # TODO comment
        pass

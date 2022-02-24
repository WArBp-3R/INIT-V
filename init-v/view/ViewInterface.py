import dash_cytoscape as cyto
from tensorflow.python.keras.callbacks import History

from controller.init_v_controll_logic import ExportOptions
from model.Configuration import Configuration
from model.RunResult import RunResult
from model.Session import Session
from model.Statistics import Statistics
from model.network.NetworkTopology import NetworkTopology


class ViewInterface:

    def create_view(self, communicator):
        """creates the page"""
        pass

    def parse_config(self, smp: int, scl: str, nrm: str, mtd: list[str], hly: int, nhl: str, lsf: str, epc: int,
                     opt: str) -> Configuration:
        """builds a config from the given values"""
        pass

    def create_run(self) -> RunResult:
        """creates a new run"""
        pass

    def get_run_list(self) -> list:
        """returns the list of runs represented by timestamps"""
        pass

    def get_method_results(self, run_timestamp) -> tuple[
        list[(float, float, str, str)], list[(float, float, str, str)]]:
        pass

    def get_performance(self, run_timestamp) -> tuple[History, list[(float, float)]]:  # TODO - define for autoencoder
        pass

    def get_network_topology(self) -> NetworkTopology:
        """returns the current network topology"""
        pass

    def get_highest_protocol_set(self) -> set[str]:
        """returns all protocols of the highest layer"""
        pass

    def get_statistics(self) -> Statistics:
        pass

    # cleanup bookmark
    def compare_runs(self, pos: list):
        pass

    def create_new_session(self, pcap_path: str):
        pass

    def load_session(self, source_path: str) -> Session:
        pass

    def load_config(self, source_path: str) -> Configuration:
        pass

    def load_topology_graph(self, source_path: str) -> cyto.Cytoscape:
        pass

    def save_session(self, output_path: str, config: Configuration, t_g: cyto.Cytoscape):
        pass

    def default_config(self):
        pass

    def set_default_config(self, lsc: int, vsc: list[str], nrm: str, mtd: list[str], hly: int, nhl: str,
                           lsf: str, epc: int, opt: str):
        pass

    def update_config(self, config: Configuration):
        pass

    def save_config(self, output_path: str, config: Configuration):
        pass

    def export(self, output_path: str, options: ExportOptions):
        pass

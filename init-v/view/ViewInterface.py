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

    def start_view(self):
        """starts the view"""

    def parse_config(self, smp: int, scl: str, nrm: str, mtd: list[str], hly: int, nhl: str, lsf: str, epc: int,
                     opt: str) -> Configuration:
        """builds a config from the given values"""
        pass

    def unpack_config(self, cfg: Configuration):
        """unpacks all config values from given configuration"""
        pass

    def get_active_config(self) -> Configuration:
        """gets active configuration from the model"""
        pass

    def update_config(self, config: Configuration):
        """updates the active configuration from the model"""
        pass

    def is_active_config_valid(self) -> bool:
        """returns if active config is volid"""
        pass

    def create_run(self) -> int:
        """creates a new run and returns id"""
        pass

    def get_run_list(self) -> list:
        """returns the list of runs represented by timestamps"""
        pass

    def get_run_configs(self, runs) -> list[Configuration]:
        """returns the configurations used in the given runs"""
        pass

    def get_method_results(self, run_timestamp) -> (
            list[(float, float, dict[str, str]), str], list[(float, float, dict[str, str]), str]):
        pass

    def get_performance(self, run_timestamp) -> (
            dict[str, list], list[(float, float)]):  # TODO - define for autoencoder
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

    def save_session(self, output_path: str, t_g: cyto.Cytoscape):
        pass

    def get_default_config(self) -> Configuration:
        pass

    def set_default_config(self, config: Configuration):
        pass

    def save_config(self, output_path: str, config: Configuration):
        pass

    def export(self, output_path: str, options: ExportOptions):
        pass

    def get_session_path(self):
        pass

from controller.init_v_controll_logic import ExportOptions
from model.network.NetworkTopology import NetworkTopology


class ViewInterface:

    def create_view(self, communicator):
        pass

    def get_run_list(self) -> list:
        pass

    def create_run(self, lsc: int, vsc: list[str], nrm: str, mtd: list[str], hly: int, nhl: str, lsf: str, epc: int,
                   opt: str):
        pass

    def get_method_results(self, run_timestamp) -> tuple[
        list[(float, float, str, str)], list[(float, float, str, str)]]:
        pass

    def get_performance(self, run_timestamp) -> list[(float, float)]:  # TODO - define for autoencoder
        pass

    def get_network_topology(self) -> NetworkTopology:
        pass

    def get_protocol_set(self) -> set[str]:
        pass

    def get_highest_protocol_set(self) -> set[str]:
        pass

    def compare_runs(self, pos: list):
        pass

    def create_new_session(self, pcap_path:str):
        pass

    def load_session(self, source_path: str):
        pass

    def load_config(self, source_path: str):
        pass

    def save_session(self, output_path: str, lsc: int, vsc: list[str], nrm: str, mtd: list[str], hly: int, nhl: str,
                     lsf: str, epc: int, opt: str):
        pass

    def default_config(self):
        pass

    def set_default_config(self):
        pass

    def save_config(self, output_path: str, lsc: int, vsc: list[str], nrm: str, mtd: list[str], hly: int, nhl: str,
                    lsf: str, epc: int, opt: str):
        pass

    def export(self, output_path: str, options: ExportOptions):
        pass

from controller.init_v_controll_logic import BackendAdapter
from model import Configuration, RunResult
from model.network import NetworkTopology,Connection,Device


class Calculator:

    def __init__(self):
        self.backend_adapter = BackendAdapter()

    def calculate_topology(self, pcap_path: str) -> NetworkTopology:
        macs,ips,connections = self.backend_adapter.get_topology_information(pcap_path)
        # TODO implementation details

    def calculate_run(self, pcap_path: str, config: Configuration) -> (RunResult, RunResult):
        pca_result: RunResult
        autoencoder_result: RunResult
        if config.autoencoder:
            autoencoder_history, autoencoder_packet_mapping = self.backend_adapter.calculate_autoencoder(pcap_path,config)
            # TODO creation of RunResult
        if config.pca:
            pca_performance, pca_packet_mapping = self.backend_adapter.calculate_pca(pcap_path,config)
            # TODO creation of RunResult
        return pca_result,autoencoder_result

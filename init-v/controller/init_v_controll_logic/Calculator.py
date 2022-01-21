from controller.init_v_controll_logic.BackendAdapter import BackendAdapter
from model.RunResult import RunResult
from model.network.NetworkTopology import NetworkTopology
from model.network.Device import Device
from model.network.Connection import Connection
from model.Configuration import Configuration


class Calculator:
    def __init__(self, pcap_path: str):
        self.backend_adapter = BackendAdapter(pcap_path)

    def calculate_topology(self) -> NetworkTopology:
        device_dict: dict[str, Device] = dict()
        connections: dict[str, Connection] = dict()
        device_macs = self.backend_adapter.get_device_macs()
        for x in device_macs:
            device_ips = list()
            ip_addresses: list = self.backend_adapter.get_associated_ips(x)
            for y in ip_addresses:
                device_ips.append(y)
            device_dict.update({x: Device(x, device_ips)})
        all_connections= self.backend_adapter.get_connections()
        for device in device_dict:
            connections: dict = all_connections.get(device)
            for protocol in connections:
                for connected_device in connections.get(protocol):
                    if connected_device not in all_connections:
                        connections.update({device: Connection(device_dict.get(device)
                                                                , device_dict.get(connected_device))})
                        # TODO add protocol of device as well
        return NetworkTopology(list(device_dict.values()), list(connections.values()))

    def calculate_run(self, pcap_path: str, config: Configuration) -> (RunResult, RunResult):
        pca_result: RunResult = RunResult()
        autoencoder_result: RunResult = RunResult()
        if config.autoencoder:
            autoencoder_history, autoencoder_packet_mapping \
                = self.backend_adapter.calculate_autoencoder(config)
            # TODO creation of RunResult
        if config.pca:
            pca_performance, pca_packet_mapping = self.backend_adapter.calculate_pca(config)
            # TODO creation of RunResult
        return pca_result, autoencoder_result



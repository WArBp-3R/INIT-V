from controller.init_v_controll_logic.BackendAdapter import BackendAdapter
from model.RunResult import RunResult
from model.network.NetworkTopology import NetworkTopology
from model.MethodResult import MethodResult
from model.PerformanceResult import PerformanceResult
from model.network.Device import Device
from model.network.Connection import Connection
from model.Configuration import Configuration
from model.Statistics import Statistics
from datetime import datetime
from scapy.packet import Packet


def _parse_packet_information(packet: Packet) -> str:
    packet_information = f"Sender MAC: {packet.getlayer(2).src}\nReceiver MAC: {packet.getlayer(2).dst}"
    ip_information = ""
    if packet.getlayer(3) is not None:
        ip_information = f"\nSender IP: {packet.getlayer(3).src}\nReceiver IP: {packet.getlayer(3).dst}"
    return packet_information + ip_information


def _parse_statistics(packet_collection: list[Packet, str]) -> Statistics:
    # TODO
    pass


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
        all_connections = self.backend_adapter.get_connections()
        for device in device_dict:
            connections: dict = all_connections.get(device)
            for protocol in connections:
                for connected_device in connections.get(protocol):
                    if connected_device not in all_connections:
                        connections.update({device: Connection(device_dict.get(device), device_dict.get(connected_device), [])})
                    elif protocol not in all_connections.get(device).protocols:
                        all_connections.get(device).append(protocol)
        return NetworkTopology(list(device_dict.values()), list(connections.values()))

    def calculate_run(self, pcap_path: str, config: Configuration) -> RunResult:
        autoencoder_result: list[float, float, str] = list()
        autoencoder_history: keras.History
        pca_result: list[float, float, str] = list()
        pca_performance: list = list()
        timestamp: datetime = datetime.now()
        if config.autoencoder:
            autoencoder_history, autoencoder_packet_mapping = self.backend_adapter.calculate_autoencoder(config)
            autoencoder_result = self._parse_method_result(autoencoder_packet_mapping)
        if config.pca:
            pca_performance, pca_packet_mapping = self.backend_adapter.calculate_pca(config)
            pca_result = self._parse_method_result(pca_packet_mapping)
        return RunResult(timestamp, config, MethodResult(pca_result, autoencoder_result), _parse_statistics(self.backend_adapter.get_packet_information())
                         , PerformanceResult(pca_performance, autoencoder_history))

    def _parse_method_result(self, mapped_packets: list[(float, float)]) -> list[(float, float, str)]:
        method_result: list[(float, float, str)] = list()
        for packet_mapping, packet_information, packet_protocol in zip(mapped_packets, self.backend_adapter.get_packet_information()):
            packet_tooltip_information: str = f"Protocol: {packet_protocol}\n" + _parse_packet_information(packet_information)
            method_result.append((packet_mapping, packet_tooltip_information))
        return method_result




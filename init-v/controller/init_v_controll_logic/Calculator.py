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


class Calculator:
    def __init__(self, pcap_path: str):
        self.backend_adapter = BackendAdapter(pcap_path)
        self.statistics: Statistics = Statistics()
        self.protocols: set[str] = set()
        self._packets: list[Packet] = self.backend_adapter.get_packet_information()
        self._device_macs: list[str] = self.backend_adapter.get_device_macs()
        self._connection_information: dict = self.backend_adapter.get_connections()
        self._connections: dict[str, Connection] = dict()
        self._devices: dict[str, Device] = dict()
        self._connection_protocol_packets: dict[Connection, dict[str, list[Packet]]] = dict()
        self._connection_packets: dict[Connection, list[Packet]] = dict()
        self._connection_statistics: dict[Connection, dict[str, str]] = dict()
        self._connection_statistics_protocol: dict[Connection, dict[str, dict[str, str]]] = dict()
        self._calculate_devices()
        self._calculate_connections()
        self._parse_connection_statistics()
        self._sort_packets()

    def _calculate_devices(self):
        for mac in self._device_macs:
            self._devices[mac] = Device(mac, self.backend_adapter.get_associated_ips(mac))

    def _calculate_connections(self):
        for device_mac in self._connection_information.keys():
            for protocol, connected_devices in self._connection_information[device_mac]:
                self.protocols.add(protocol)
                for connected_device in connected_devices:
                    if connected_device in self._connections.keys():
                        self._connections[connected_device].protocols.add(protocol)
                    else:
                        if device_mac not in self._connections.keys():
                            self._connections[device_mac] = Connection(device_mac, connected_device, {protocol}, "",
                                                                       dict())
                        else:
                            self._connections[device_mac].protocols.add(protocol)

    def _sort_packets(self):
        for packet, protocol in self._packets:
            sender_mac = packet.getlayer(2)
            receiver_mac = packet.getlayer(2)
            packet_connection: Connection
            if sender_mac in self._connections.keys():
                packet_connection = self._connections[sender_mac]
            else:
                packet_connection = self._connections[receiver_mac]
            if protocol not in self._connection_protocol_packets[packet_connection].keys():
                self._connection_protocol_packets[packet_connection][protocol] = list()
            if packet_connection not in self._connection_packets.keys():
                self._connection_packets[packet_connection] = list()
            self._connection_protocol_packets[packet_connection][protocol].append(packet)
            self._connection_packets[packet_connection].append(packet)

    def _parse_connection_statistics(self):
        for connection in self._connections.values():
            self._connection_statistics[connection] = dict()
            self._connection_statistics_protocol[connection] = dict()
            self._connection_statistics[connection]["Packet Count"] = str(len(self._connection_packets[connection]))
            for protocol, protocol_packets in self._connection_protocol_packets[connection]:
                self._connection_statistics_protocol[connection][protocol] = dict()
                self._connection_statistics_protocol[connection][protocol]["Packet Count"] \
                    = str(len(self._connection_protocol_packets[connection][protocol]))
            # TODO

    def calculate_topology(self) -> NetworkTopology:
        return NetworkTopology(list(self._devices.values()), list(self._connections.values()))

    def calculate_run(self, config: Configuration) -> RunResult:
        autoencoder_result: list[float, float, str] = list()
        autoencoder_history: keras.History = History()
        pca_result: list[float, float, str] = list()
        pca_performance: list = list()
        timestamp: datetime = datetime.now()
        if config.autoencoder:
            autoencoder_history, autoencoder_packet_mapping = self.backend_adapter.calculate_autoencoder(config)
            autoencoder_result = self._parse_method_result(autoencoder_packet_mapping)
        if config.pca:
            pca_performance, pca_packet_mapping = self.backend_adapter.calculate_pca(config)
            pca_result = self._parse_method_result(pca_packet_mapping)
        return RunResult(timestamp, config, MethodResult(pca_result, autoencoder_result),
                         PerformanceResult(pca_performance, autoencoder_history))

    def _parse_method_result(self, mapped_packets: list[(float, float)]) -> list[(float, float, str)]:
        method_result: list[(float, float, str)] = list()
        for packet_mapping, packet_information, packet_protocol in \
                zip(mapped_packets, self.backend_adapter.get_packet_information()):
            packet_tooltip_information: str = f"Protocol: {packet_protocol}\n" \
                                              + _parse_packet_information(packet_information)
            method_result.append((packet_mapping, packet_tooltip_information))
        return method_result

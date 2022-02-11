import plotly.express as px
from tensorflow.python.keras.callbacks import History

from controller.init_v_controll_logic.BackendAdapter import BackendAdapter
from model.RunResult import RunResult
from model.network.NetworkTopology import NetworkTopology
from model.MethodResult import MethodResult
from model.PerformanceResult import PerformanceResult
from model.network.Device import Device
from model.network.Connection import Connection
from model.Configuration import Configuration
from model.Statistics import Statistics
from datetime import datetime, timedelta
from scapy.packet import Packet
from scapy.layers.inet import *

def _parse_packet_information(packet: Packet) -> str:
    packet_information = f"Sender MAC: {packet.src}\nReceiver MAC: {packet.dst}"
    ip_information = ""
    ip_layer = packet.getlayer(IP)
    if ip_layer is not None:
        ip_information = f"\nSender IP: {ip_layer.src}\nReceiver IP: {ip_layer.dst}"
    return packet_information + ip_information

def _find_oldest_newest_packet(packets: list[Packet]) -> (Packet, Packet):
    oldest_packet = packets[0]
    newest_packet = packets[0]
    for packet in packets:
        if packet.time > newest_packet.time:
            newest_packet = packet
        elif packet.time < oldest_packet.time:
            oldest_packet = packet
    return oldest_packet,newest_packet


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
        self._connection_oldest_newest_packets: dict[Connection, (Packet, Packet)] = dict()
        self._connection_oldest_newest_protocol_packets: dict[Connection, dict[str, (Packet, Packet)]] = dict()
        self._connection_packets: dict[Connection, list[Packet]] = dict()
        self._connection_statistics: dict[Connection, dict[str, str]] = dict()
        self._connection_statistics_protocol: dict[Connection, dict[str, dict[str, str]]] = dict()
        self._sent_received_packet_count: dict[str, (int, int)] = dict()
        self._calculate_devices()
        self._calculate_connections()
        self._sort_packets()
        self._parse_connection_statistics()
        # self._calculate_figures()

    def _calculate_devices(self):
        for mac in self._device_macs:
            self._devices[mac] = Device(mac, self.backend_adapter.get_associated_ips(mac))
            self._sent_received_packet_count[mac] = (0, 0)

    def _calculate_connections(self):
        for device_mac in self._connection_information.keys():
            connections_per_protocol = self._connection_information[device_mac]
            for protocol in connections_per_protocol.keys():
                self.protocols.add(protocol)
                for connected_device in connections_per_protocol[protocol]:
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
            sender_mac = packet.src
            receiver_mac = packet.dst
            srpc_first = self._sent_received_packet_count[sender_mac][0] + 1
            srpc_second = self._sent_received_packet_count[sender_mac][1] + 1
            self._sent_received_packet_count[sender_mac] = (srpc_first, srpc_second)
            packet_connection: Connection

            if sender_mac in self._connections.keys():
                packet_connection = self._connections[sender_mac]
            else:
                packet_connection = self._connections[receiver_mac]

            if packet_connection not in self._connection_protocol_packets.keys():
                self._connection_protocol_packets[packet_connection] = dict()
            if packet_connection not in self._connection_packets.keys():
                self._connection_packets[packet_connection] = list()
            if protocol not in self._connection_protocol_packets[packet_connection].keys():
                self._connection_protocol_packets[packet_connection][protocol] = list()

            self._connection_protocol_packets[packet_connection][protocol].append(packet)
            self._connection_packets[packet_connection].append(packet)

    def _parse_connection_statistics(self):
        for connection in self._connections.values():
            self._connection_statistics[connection] = dict()
            self._connection_statistics_protocol[connection] = dict()
            self._connection_oldest_newest_packets[connection] = (
            self._connection_packets[connection][0], self._connection_packets[connection][0])
            self._connection_statistics[connection]["Packet Count"] = str(len(self._connection_packets[connection]))
            for protocol, protocol_packets in self._connection_protocol_packets[connection].items():
                oldest_packet, newest_packet = _find_oldest_newest_packet(protocol_packets)
                if connection not in self._connection_oldest_newest_protocol_packets.keys():
                    self._connection_oldest_newest_protocol_packets[connection] = dict()
                self._connection_oldest_newest_protocol_packets[connection][protocol] = (oldest_packet, newest_packet)
                if self._connection_oldest_newest_packets[connection][0] > oldest_packet:
                    self._connection_oldest_newest_packets[connection][0] = oldest_packet
                if self._connection_packets[connection][1] < newest_packet:
                    self._connection_packets[connection][1] = newest_packet
                self._connection_statistics_protocol[connection][protocol] = dict()
                self._connection_statistics_protocol[connection][protocol]["Packet Count"] \
                    = str(len(self._connection_protocol_packets[connection][protocol]))
            self._calculate_throughput()

    def _calculate_throughput(self):
        for connection in self._connections.values():
            packet_count: int = int(self._connection_statistics[connection]["Packet Count"])
            total_time: timedelta = datetime.fromtimestamp(self._connection_oldest_newest_packets[connection][1].time) \
                                    - datetime.fromtimestamp(self._connection_oldest_newest_packets[connection][0].time)
            self._connection_statistics[connection]["Packets per second"] = str(
                total_time.total_seconds() / packet_count)
            for protocol in self._connection_protocol_packets[connection].keys():
                protocol_packet_count: int = int(self._connection_statistics_protocol[connection][protocol]
                                                 ["Packet Count"])
                protocol_packet_total_time: timedelta = datetime.fromtimestamp(
                    self._connection_oldest_newest_protocol_packets[connection][protocol][1].time) \
                                                        - datetime.fromtimestamp(
                    self._connection_oldest_newest_protocol_packets[connection][protocol][0].time)
                self._connection_statistics_protocol[connection][protocol]["Packets per second"] \
                    = str(protocol_packet_total_time.total_seconds() / protocol_packet_count)

    def _update_connection_information(self):
        for connection in self._connections.values():
            connection_statistics = self._connection_statistics[connection]
            connection_statistics_str = ""
            for stat_name, stat_value in connection_statistics:
                connection_statistics = connection_statistics + f"{stat_name}: {stat_value}\n"
                for protocol, protocol_statistics in self._connection_statistics_protocol[connection]:
                    protocol_statistics_str = ""
                    for protocol_stat_name, protocol_stat_value in protocol_statistics:
                        protocol_statistics_str = protocol_statistics_str \
                                                  + f"{protocol_stat_name}: {protocol_stat_value}\n"
                    connection.protocol_connection_information[protocol] = protocol_statistics_str
            connection.connection_information = connection_statistics_str

    def calculate_topology(self) -> NetworkTopology:
        return NetworkTopology(list(self._devices.values()), list(self._connections.values()))

    def calculate_run(self, config: Configuration) -> RunResult:
        autoencoder_result: list[float, float, str] = list()
        autoencoder_history: History = History()
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

    def calculate_statistics(self):
        return self.statistics

    # def _parse_method_result(self, mapped_packets: list[(float, float)]) -> list[(float, float, str)]:
    #     method_result: list[(float, float, str)] = list()
    #     for packet_mapping, packet_information, packet_protocol in \
    #             zip(mapped_packets, self.backend_adapter.get_packet_information()):
    #         packet_tooltip_information: str = f"Protocol: {packet_protocol}\n" \
    #                                           + _parse_packet_information(packet_information)
    #         method_result.append((packet_mapping, packet_tooltip_information))
    #     return method_result

    def _parse_method_result(self, mapped_packets: list[(float, float)]) -> list[(float, float, str)]:
        method_result: list[(float, float, str)] = list()
        for packet_mapping, packet_information in zip(mapped_packets, self.backend_adapter.get_packet_information()):
            packet_tooltip_information: str = f"Protocol: {packet_information[1]}\n" \
                                              + _parse_packet_information(packet_information[0])
            method_result.append((min(packet_mapping), max(packet_mapping), packet_tooltip_information))
        return method_result

    def _calculate_figures(self):
        self._calculate_sent_received_packets_figure()

    def _calculate_sent_received_packets_figure(self):
        packets_sent_received_data = dict({"Packets sent": list(), "Packets received": list(), "mac address": list})
        for mac, (sent_packets, received_packets) in self._sent_received_packet_count.items():
            packets_sent_received_data["Packets sent"] = sent_packets
            packets_sent_received_data["Packets received"] = received_packets
            packets_sent_received_data["mac address"] = mac
        self.statistics.statistics["Total packets sent and received"] = px.scatter(packets_sent_received_data,
                                                                                   x="Packets sent",
                                                                                   y="Packets received",
                                                                                   hover_data=["mac address"])
        self.statistics.statistics["Total packets sent"] = px.bar(packets_sent_received_data, x="mac address",
                                                                  y="Packets sent",
                                                                  hover_data=["mac address", "Packets sent"])
        self.statistics.statistics["Total packets received"] = px.bar(packets_sent_received_data, x="mac address",
                                                                      y="Packets received",
                                                                      hover_data=["mac address", "Packets received"])

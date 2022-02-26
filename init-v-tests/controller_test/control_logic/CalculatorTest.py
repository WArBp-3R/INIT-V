import json
from controller.init_v_controll_logic.Calculator import Calculator
from model.network.NetworkTopology import NetworkTopology
from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from model.RunResult import RunResult
from model.MethodResult import MethodResult
from datetime import datetime
from keras.callbacks import History

# Define constants
RESOURCE_FOLDER_PATH = "..\\..\\resources\\pcap files\\"
PCAP_NAME = "pcap_name"
PACKET_COUNT = "packet_count"
CONNECTION_COUNT = "connection_count"
DEVICE_COUNT = "device_count"
SAMPLE_CONFIG = Configuration(True, True, 100, "Length", "None", AutoencoderConfiguration(4, [2, 4, 8, 16], "MSE", 10,
                                                                                          "adam"))

# Load resource json file for packet information
test_pcap_json_file = open(f"{RESOURCE_FOLDER_PATH}pcap_properties.json")
test_pcap_files = json.load(test_pcap_json_file)
test_pcap_json_file.close()


def calculate_connection_count(network: NetworkTopology) -> int:
    connection_count = 0
    for connection in network.connections:
        connection_count += len(connection.protocols)
    return int(connection_count / 2)


def test_network_topology():
    """
    Tests if the created network topology has the correct amount of devices and connections.
    """
    for pcap_file in test_pcap_files:
        calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        topology = calculator.calculate_topology()
        assert calculate_connection_count(topology) == pcap_file[CONNECTION_COUNT]
        assert len(topology.devices) == pcap_file[DEVICE_COUNT]


def test_packet_per_second_data():
    """
    Tests if the oldest packet of a connection is older than the newest packet.
    """
    for pcap_file in test_pcap_files:
        calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        all_connections_data = calculator._connection_oldest_newest_packets
        all_connections_per_protocol_data = calculator._connection_oldest_newest_protocol_packets
        for (oldest_packet, newest_packet) in all_connections_data.values():
            assert oldest_packet.time <= newest_packet.time
        for (oldest_packet, newest_packet) in all_connections_per_protocol_data.values():
            assert oldest_packet.time <= newest_packet.time


def test_packet_sort():
    """
    Tests if the packets were sorted correctly in a private variable.
    """
    for pcap_file in test_pcap_files:
        calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        sorted_packets = calculator._connection_packets.values()
        for packets in sorted_packets:
            src_mac = packets[0].src
            dst_mac = packets[0].dst
            for packet in packets:
                assert (packet.src == src_mac and packet.dst == dst_mac) or \
                       (packet.src == dst_mac and packet.dst == src_mac)


def test_packet_count():
    """
    Tests if the packet count is correct in various data saved in the calculator class.
    Sum of all packets sent = Sum of all packets received = Sum of the highest protocols' usage count
    Each of these mentioned sums should be equal to the packet count.
    """
    for pcap_file in test_pcap_files:
        calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        packet_counts = calculator._sent_received_packet_count.values()
        sent_packet_sum = 0
        received_packet_sum = 0
        highest_protocol_count_sum = 0
        for (sent_packets, received_packets) in packet_counts:
            sent_packet_sum += sent_packets
            received_packet_sum += received_packets
        for highest_protocol_count in calculator._protocols_use_count.values():
            highest_protocol_count_sum += highest_protocol_count
        assert sent_packet_sum == pcap_file[PACKET_COUNT]
        assert received_packet_sum == pcap_file[PACKET_COUNT]
        assert highest_protocol_count_sum == pcap_file[PACKET_COUNT]


def test_autoencoder_pca():
    """
    Tests the autoencoder and pca.

    Checks if the timestamp is after the invocation time of the calculate_run method,
    the total mappings received should be equal to the packet count, the config of the result should be the same config
    that was passed along the calculate_run method and finally the performance analysis of the pca should be a
    two-dimensional tuple whereas the type of the autoencoder performance analysis should be a History object.
    """
    for pcap_file in test_pcap_files:
        calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        current_timestamp = datetime.now().timestamp()
        run_result = calculator.calculate_run(SAMPLE_CONFIG)
        assert current_timestamp <= run_result.timestamp.timestamp()
        assert len(run_result.result.pca_result) == pcap_file[PACKET_COUNT]
        assert len(run_result.result.autoencoder_result) == pcap_file[PACKET_COUNT]
        assert run_result.config == SAMPLE_CONFIG
        assert type(run_result.analysis.autoencoder) is History
        assert type(run_result.analysis.pca) is tuple[float, float]

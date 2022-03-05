import json
import os
import random
import plotly.express as px
import pytest
from scapy.layers.l2 import Ether

from controller.init_v_controll_logic.Calculator import Calculator
from model.network.NetworkTopology import NetworkTopology
from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from datetime import datetime
from keras.callbacks import History

# Define constants
RESOURCE_FOLDER_PATH = os.path.abspath(f"..{os.sep}..{os.sep}resources{os.sep}pcap files") + os.sep
PCAP_NAME = "pcap_name"
PACKET_COUNT = "packet_count"
CONNECTION_COUNT = "connection_count"
DEVICE_COUNT = "device_count"
SAMPLE_CONFIG = Configuration(True, True, 100, "Length", "None", AutoencoderConfiguration(4, [2, 4, 8, 16], "MSE", 10, "adam"))
SAMPLE_CONFIG_ONLY_PCA = Configuration(False, True, 100, "Length", "None", AutoencoderConfiguration(4, [2, 4, 8, 16], "MSE", 10, "adam"))
SAMPLE_CONFIG_ONLY_AUTOENCODER = Configuration(True, False, 100, "Length", "None", AutoencoderConfiguration(4, [2, 4, 8, 16], "MSE", 10, "adam"))
SAMPLE_CONFIG_NO_AUTOENCODER_PCA = Configuration(False, False, 100, "Length", "None", AutoencoderConfiguration(4, [2, 4, 8, 16], "MSE", 10, "adam"))

# Create output log folder and log text file
TIMESTAMP = datetime.now()
OUTPUT_FOLDER = os.path.abspath(f"..{os.sep}..{os.sep}..{os.sep}test_outputs") + os.sep
TEST_OUTPUT_FOLDER = OUTPUT_FOLDER + f"CalculatorTest_{TIMESTAMP.hour}{TIMESTAMP.minute}{TIMESTAMP.second}"
if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)
os.mkdir(TEST_OUTPUT_FOLDER)
OUTPUT_FILE = open(f"{TEST_OUTPUT_FOLDER}{os.sep}log.txt", "w")

# Statistical data collections:
CALCULATOR_INIT_DICT = {"Packet count": list(), "Time (seconds)": list(), "Title": "Calculator Initialization Time"}
CALCULATE_TOPOLOGY_DICT = {"Packet count": list(), "Time (seconds)": list(), "Title": "Calculate Topology Time"}
STATISTICS_LIST = [CALCULATOR_INIT_DICT, CALCULATE_TOPOLOGY_DICT]

# Load resource json file for packet information
test_pcap_json_file = open(f"{RESOURCE_FOLDER_PATH}pcap_properties.json")
test_pcap_files = json.load(test_pcap_json_file)[0:-3] #list(filter(lambda x: x[PACKET_COUNT] <= 1000000, json.load(test_pcap_json_file)[0:-3]))
test_pcap_json_file.close()


def _calculate_connection_count(network: NetworkTopology) -> int:
    connection_count = 0
    for connection in network.connections:
        connection_count += len(connection.protocols)
    return connection_count


def _print_log(log_text: str):
    print(log_text)
    OUTPUT_FILE.write(f"{log_text}\n")


def teardown_module():
    global OUTPUT_FILE
    OUTPUT_FILE.close()
    for i, stat_dict in enumerate(STATISTICS_LIST):
        figure = px.scatter(stat_dict, x="Packet count", y="Time (seconds)", title=stat_dict["Title"])
        title = stat_dict["Title"]
        figure.write_image(f"{TEST_OUTPUT_FOLDER}{os.sep}{title}.png")


def startup_test():
    random.shuffle(test_pcap_files)


@pytest.mark.parametrize("pcap_data", test_pcap_files)
def test_network_topology(pcap_data):
    """
    Tests if the created network topology has the correct number of devices and connections created.
    """
    _print_log("\nStarting network topology test")
    _print_log(f"[{datetime.now()}]: testing {pcap_data[PCAP_NAME]} ({pcap_data[PACKET_COUNT]} packets)...")
    calculator_init_time = datetime.now()
    calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_data[PCAP_NAME]}")
    calculator_init_time = datetime.now() - calculator_init_time
    calculate_topology_time = datetime.now()
    topology = calculator.calculate_topology()
    calculate_topology_time = datetime.now() - calculate_topology_time
    CALCULATOR_INIT_DICT["Packet count"].append(pcap_data[PACKET_COUNT])
    CALCULATOR_INIT_DICT["Time (seconds)"].append(calculator_init_time.total_seconds())
    CALCULATE_TOPOLOGY_DICT["Packet count"].append(pcap_data[PACKET_COUNT])
    CALCULATE_TOPOLOGY_DICT["Time (seconds)"].append(calculate_topology_time.total_seconds())
    _print_log(f"Calculator initialization time: {calculator_init_time}\n"
                f"Calculate topology time: {calculate_topology_time}")
    assert _calculate_connection_count(topology) == pcap_data[CONNECTION_COUNT]
    assert len(topology.devices) == pcap_data[DEVICE_COUNT]
    _print_log(f"[{datetime.now()}]: Test passed.")


@pytest.mark.parametrize("pcap_data", test_pcap_files)
def test_packet_per_second_data(pcap_data):
    """
    Tests if the oldest packet of a connection is older than the newest packet in a private variable used for the
    calculation of the packets per second.
    """
    _print_log("\nStarting packets per second data test.")
    _print_log(f"[{datetime.now()}]: testing {pcap_data[PCAP_NAME]} ({pcap_data[PACKET_COUNT]} packets)...")
    calculator_init_time = datetime.now()
    calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_data[PCAP_NAME]}")
    calculator_init_time = datetime.now() - calculator_init_time
    CALCULATOR_INIT_DICT["Packet count"].append(pcap_data[PACKET_COUNT])
    CALCULATOR_INIT_DICT["Time (seconds)"].append(calculator_init_time.total_seconds())
    _print_log(f"Calculator initialization time: {calculator_init_time}")
    all_connections_data = calculator._connection_oldest_newest_packets
    all_connections_per_protocol_data_dicts = calculator._connection_oldest_newest_protocol_packets.values()
    all_protocol_pairs = list()
    for protocol_dict in all_connections_per_protocol_data_dicts:
        for pair in protocol_dict.values():
            all_protocol_pairs.append(pair)
    for (oldest_packet, newest_packet) in all_connections_data.values():
        assert oldest_packet.time <= newest_packet.time
    for (oldest_packet, newest_packet) in all_protocol_pairs:
        assert oldest_packet.time <= newest_packet.time
    _print_log(f"[{datetime.now()}]: Test passed.")


@pytest.mark.parametrize("pcap_data", test_pcap_files)
def test_packet_sort(pcap_data):
    """
    Tests if the packets were sorted correctly in a private variable according to their connections.
    """
    _print_log("\nStarting packet sort test.")
    _print_log(f"[{datetime.now()}]: testing {pcap_data[PCAP_NAME]} ({pcap_data[PACKET_COUNT]} packets)...")
    calculator_init_time = datetime.now()
    calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_data[PCAP_NAME]}")
    calculator_init_time = datetime.now() - calculator_init_time
    CALCULATOR_INIT_DICT["Packet count"].append(pcap_data[PACKET_COUNT])
    CALCULATOR_INIT_DICT["Time (seconds)"].append(calculator_init_time.total_seconds())
    _print_log(f"Calculator initialization time: {calculator_init_time}")
    for connection, connection_packets in calculator._connection_packets.items():
        src_mac = connection.first_device.mac_address
        dst_mac = connection.second_device.mac_address
        for packet in connection_packets:
            assert (packet[Ether].src == src_mac and packet[Ether].dst == dst_mac) or \
                   (packet[Ether].src == dst_mac and packet[Ether].dst == src_mac)
    _print_log(f"[{datetime.now()}]: Test passed.")


@pytest.mark.parametrize("pcap_data", test_pcap_files)
def test_packet_count(pcap_data):
    """
    Tests if the packet number is correct in various data saved in the calculator class.
    Sum of all packets sent = Sum of all packets received = Sum of the highest protocols' usage count
    Each of these mentioned sums should be equal to the packet count.
    """
    _print_log("\nStarting packet count test")
    _print_log(f"[{datetime.now()}]: testing {pcap_data[PCAP_NAME]} ({pcap_data[PACKET_COUNT]} packets)...")
    calculator_init_time = datetime.now()
    calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_data[PCAP_NAME]}")
    calculator_init_time = datetime.now() - calculator_init_time
    CALCULATOR_INIT_DICT["Packet count"].append(pcap_data[PACKET_COUNT])
    CALCULATOR_INIT_DICT["Time (seconds)"].append(calculator_init_time.total_seconds())
    _print_log(f"Calculator initialization time: {calculator_init_time}")
    packet_counts = calculator._sent_received_packet_count.values()
    sent_packet_sum = 0
    received_packet_sum = 0
    highest_protocol_count_sum = 0
    for (sent_packets, received_packets) in packet_counts:
        sent_packet_sum += sent_packets
        received_packet_sum += received_packets
    for highest_protocol_count in calculator._protocols_use_count.values():
        highest_protocol_count_sum += highest_protocol_count
    assert sent_packet_sum == pcap_data[PACKET_COUNT] or calculator._contains_non_ether_packets
    assert received_packet_sum == pcap_data[PACKET_COUNT] or calculator._contains_non_ether_packets
    assert highest_protocol_count_sum == pcap_data[PACKET_COUNT]
    _print_log(f"[{datetime.now()}]: Test passed.")


@pytest.mark.skip("It works, takes an eternity to work, so ignoring this case.")
@pytest.mark.parametrize("pcap_data", test_pcap_files)
def test_autoencoder_pca(pcap_data):
    """
    Tests if the results of the autoencoder and pca are correct.

    Checks if the timestamp is after the invocation time of the calculate_run method,
    the total mappings received should be equal to the packet count, the config of the result should be the same config
    that was passed along the calculate_run method and finally the performance analysis of the pca should be a
    two-dimensional tuple whereas the type of the autoencoder performance analysis should be a History object.
    """
    _print_log("\nStarting autoencoder pca test.")
    _print_log(f"[{datetime.now()}]: testing {pcap_data[PCAP_NAME]} ({pcap_data[PACKET_COUNT]} packets)...")
    calculator_init_time = datetime.now()
    calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_data[PCAP_NAME]}")
    calculator_init_time = datetime.now() - calculator_init_time
    CALCULATOR_INIT_DICT["Packet count"].append(pcap_data[PACKET_COUNT])
    CALCULATOR_INIT_DICT["Time (seconds)"].append(calculator_init_time.total_seconds())
    _print_log(f"Calculator initialization time: {calculator_init_time}")
    current_timestamp = datetime.now().timestamp()
    run_result = calculator.calculate_run(SAMPLE_CONFIG)
    assert current_timestamp <= run_result.timestamp.timestamp()
    assert len(run_result.result.pca_result) == pcap_data[PACKET_COUNT]
    assert len(run_result.result.autoencoder_result) == pcap_data[PACKET_COUNT]
    assert run_result.config == SAMPLE_CONFIG
    assert type(run_result.analysis.autoencoder) is History
    assert type(run_result.analysis.pca) is tuple
    _print_log(f"[{datetime.now()}]: Test passed.")


@pytest.mark.skip("It works, takes an eternity to work, so ignoring this case.")
@pytest.mark.parametrize("pcap_data", test_pcap_files)
def test_autoencoder_pca_configuration(pcap_data):
    """
    Tests if the RunResult contents are correct when the autoencoder and/or pca are disabled.
    """
    _print_log("\nStarting autoencoder pca configuration test")
    _print_log(f"[{datetime.now()}]: testing {pcap_data[PCAP_NAME]} ({pcap_data[PACKET_COUNT]} packets)...")
    calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_data[PCAP_NAME]}")
    run_result = calculator.calculate_run(SAMPLE_CONFIG_ONLY_AUTOENCODER)
    assert run_result.result.pca_result is None
    assert run_result.analysis.pca is None
    assert run_result.analysis.autoencoder is not None
    assert run_result.result.autoencoder_result is not None
    run_result = calculator.calculate_run(SAMPLE_CONFIG_ONLY_PCA)
    assert run_result.result.pca_result is not None
    assert run_result.analysis.pca is not None
    assert run_result.analysis.autoencoder is None
    assert run_result.result.autoencoder_result is None
    run_result = calculator.calculate_run(SAMPLE_CONFIG_NO_AUTOENCODER_PCA)
    assert run_result.result.pca_result is None
    assert run_result.analysis.pca is None
    assert run_result.analysis.autoencoder is None
    assert run_result.result.autoencoder_result is None
    _print_log(f"[{datetime.now()}]: Test passed.")

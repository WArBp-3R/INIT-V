import json
import os
import random
import plotly.express as px
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
SAMPLE_CONFIG_ONLY_PCA = Configuration(True, False, 100, "Length", "None", AutoencoderConfiguration(4, [2, 4, 8, 16], "MSE", 10, "adam"))
SAMPLE_CONFIG_ONLY_AUTOENCODER = Configuration(False, True, 100, "Length", "None", AutoencoderConfiguration(4, [2, 4, 8, 16], "MSE", 10, "adam"))
SAMPLE_CONFIG_NO_AUTOENCODER_PCA = Configuration(False, False, 100, "Length", "None", AutoencoderConfiguration(4, [2, 4, 8, 16], "MSE", 10, "adam"))

# Statistical data collections:
CALCULATOR_INIT_DICT = {"Packet count": list(), "Time (seconds)": list(), "Title": "Calculator Initialization Time"}
CALCULATE_TOPOLOGY_DICT = {"Packet count": list(), "Time (seconds)": list(), "Title": "Calculate Topology Time"}
STATISTICS_LIST = [CALCULATOR_INIT_DICT, CALCULATE_TOPOLOGY_DICT]

# Load resource json file for packet information
test_pcap_json_file = open(f"{RESOURCE_FOLDER_PATH}pcap_properties.json")
test_pcap_files = [pcap_file for pcap_file in json.load(test_pcap_json_file) if pcap_file[PACKET_COUNT] < 1000000]
test_pcap_json_file.close()


def calculate_connection_count(network: NetworkTopology) -> int:
    connection_count = 0
    for connection in network.connections:
        connection_count += len(connection.protocols)
    return connection_count


def teardown_module():
    output_folder = os.path.abspath(f"..{os.sep}..{os.sep}output") + os.sep
    for i, stat_dict in enumerate(STATISTICS_LIST):
        figure = px.scatter(stat_dict, x="Packet count", y="Time (seconds)", title=stat_dict["Title"])
        title = stat_dict["Title"]
        figure.write_image(f"{output_folder}{title}.png")


def test_network_topology():
    """
    Tests if the created network topology has the correct number of devices and connections created.
    """
    print("\nStarting network topology test")
    random.shuffle(test_pcap_files)
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        calculator_init_time = datetime.now()
        calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        calculator_init_time = datetime.now() - calculator_init_time
        calculate_topology_time = datetime.now()
        topology = calculator.calculate_topology()
        calculate_topology_time = datetime.now() - calculate_topology_time
        CALCULATOR_INIT_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        CALCULATOR_INIT_DICT["Time (seconds)"].append(calculator_init_time.total_seconds())
        CALCULATE_TOPOLOGY_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        CALCULATE_TOPOLOGY_DICT["Time (seconds)"].append(calculate_topology_time.total_seconds())
        print(f"Calculator initialization time: {calculator_init_time}"
              f"Calculate topology time: {calculate_topology_time}", sep="\n")
        assert calculate_connection_count(topology) == pcap_file[CONNECTION_COUNT]
        assert len(topology.devices) == pcap_file[DEVICE_COUNT]
        print("Test case passed.")


def test_packet_per_second_data():
    """
    Tests if the oldest packet of a connection is older than the newest packet in a private variable used for the
    calculation of the packets per second.
    """
    random.shuffle(test_pcap_files)
    print("\nStarting packets per second data test.")
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        calculator_init_time = datetime.now()
        calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        calculator_init_time = datetime.now() - calculator_init_time
        CALCULATOR_INIT_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        CALCULATOR_INIT_DICT["Time (seconds)"].append(calculator_init_time.total_seconds())
        print(f"Calculator initialization time: {calculator_init_time}")
        all_connections_data = calculator._connection_oldest_newest_packets
        all_connections_per_protocol_data = calculator._connection_oldest_newest_protocol_packets
        for (oldest_packet, newest_packet) in all_connections_data.values():
            assert oldest_packet.time <= newest_packet.time
        for (oldest_packet, newest_packet) in all_connections_per_protocol_data.values():
            assert oldest_packet.time <= newest_packet.time
        print("Test case passed.")


def test_packet_sort():
    """
    Tests if the packets were sorted correctly in a private variable according to their connections.
    """
    print("\nStarting packet sort test.")
    random.shuffle(test_pcap_files)
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        calculator_init_time = datetime.now()
        calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        calculator_init_time = datetime.now() - calculator_init_time
        CALCULATOR_INIT_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        CALCULATOR_INIT_DICT["Time (seconds)"].append(calculator_init_time.total_seconds())
        print(f"Calculator initialization time: {calculator_init_time}")
        for connection, connection_packets in calculator._connection_packets.items():
            src_mac = connection.first_device
            dst_mac = connection.second_device
            for packet in connection_packets:
                assert (packet.src == src_mac and packet.dst == dst_mac) or \
                       (packet.src == dst_mac and packet.dst == src_mac)
        print("Test case passed.")


def test_packet_count():
    """
    Tests if the packet number is correct in various data saved in the calculator class.
    Sum of all packets sent = Sum of all packets received = Sum of the highest protocols' usage count
    Each of these mentioned sums should be equal to the packet count.
    """
    print("\nStarting packet count test")
    random.shuffle(test_pcap_files)
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        calculator_init_time = datetime.now()
        calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        calculator_init_time = datetime.now() - calculator_init_time
        CALCULATOR_INIT_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        CALCULATOR_INIT_DICT["Time (seconds)"].append(calculator_init_time.total_seconds())
        print(f"Calculator initialization time: {calculator_init_time}")
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
        print("Test case passed.")


def test_autoencoder_pca():
    """
    Tests if the results of the autoencoder and pca are correct.

    Checks if the timestamp is after the invocation time of the calculate_run method,
    the total mappings received should be equal to the packet count, the config of the result should be the same config
    that was passed along the calculate_run method and finally the performance analysis of the pca should be a
    two-dimensional tuple whereas the type of the autoencoder performance analysis should be a History object.
    """
    print("\nStarting autoencoder pca test.")
    random.shuffle(test_pcap_files)
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        calculator_init_time = datetime.now()
        calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        calculator_init_time = datetime.now() - calculator_init_time
        CALCULATOR_INIT_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        CALCULATOR_INIT_DICT["Time (seconds)"].append(calculator_init_time.total_seconds())
        print(f"Calculator initialization time: {calculator_init_time}")
        current_timestamp = datetime.now().timestamp()
        run_result = calculator.calculate_run(SAMPLE_CONFIG)
        assert current_timestamp <= run_result.timestamp.timestamp()
        assert len(run_result.result.pca_result) == pcap_file[PACKET_COUNT]
        assert len(run_result.result.autoencoder_result) == pcap_file[PACKET_COUNT]
        assert run_result.config == SAMPLE_CONFIG
        assert type(run_result.analysis.autoencoder) is History
        assert type(run_result.analysis.pca) is tuple[float, float]
        print("Test case passed.")


def test_autoencoder_pca_configuration():
    """
    Tests if the RunResult contents are correct when the autoencoder and/or pca are disabled.
    """
    print("\nStarting autoencoder pca configuration test")
    random.shuffle(test_pcap_files)
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        calculator = Calculator(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
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
        print("Test case passed.")

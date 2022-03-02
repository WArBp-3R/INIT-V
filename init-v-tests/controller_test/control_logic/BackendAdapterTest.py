import json
import os
import random
import plotly.express as px
from datetime import datetime
from controller.init_v_controll_logic.BackendAdapter import BackendAdapter

# Define constants
RESOURCE_FOLDER_PATH = os.path.abspath(f"..{os.sep}..{os.sep}resources{os.sep}pcap files") + os.sep
PCAP_NAME = "pcap_name"
PACKET_COUNT = "packet_count"
CONNECTION_COUNT = "connection_count"
DEVICE_COUNT = "device_count"

UPDATE_PCAP_DICT = {"Packet count": list(), "Time (seconds)": list(), "Title": "Update PCAP Time"}
INIT_BACKEND_DICT = {"Packet count": list(), "Time (seconds)": list(), "Title": "BackendAdapter Initialization Time"}
GET_PACKET_DICT = {"Packet count": list(), "Time (seconds)": list(), "Title": "get_packet_information() Time"}
GET_DEVICES_DICT = {"Packet count": list(), "Time (seconds)": list(), "Title": "get_devices() Time"}
GET_CONNECTIONS_DICT = {"Packet count": list(), "Time (seconds)": list(), "Title": "get_connections() Time"}
STATISTICS_LIST = [UPDATE_PCAP_DICT, INIT_BACKEND_DICT, GET_PACKET_DICT, GET_DEVICES_DICT, GET_CONNECTIONS_DICT]


# Load resource json file for packet information
test_pcap_json_file = open(f"{RESOURCE_FOLDER_PATH}pcap_properties.json")
test_pcap_files = [pcap_file for pcap_file in json.load(test_pcap_json_file) if pcap_file[PACKET_COUNT] <= 500000]
test_pcap_json_file.close()


def calculate_connection_count(connections: dict[str, dict[str, list[str]]]) -> int:
    """
    Calculates the total connection count of a connection dictionary.

    Uses the handshake lemma for the calculation.
    :param connections: The connection dictionary. Format of the dictionary explained in the BackendInterface method
    document for the method get_connections.
    :return: The total count of connections.
    """
    connection_count = 0
    for connection_details in connections.values():
        for protocol, connected_devices in connection_details.items():
            connection_count += len(connected_devices)
    return int(connection_count / 2)


def teardown_module():
    output_folder = os.path.abspath(f"..{os.sep}..{os.sep}output") + os.sep
    for i, stat_dict in enumerate(STATISTICS_LIST):
        figure = px.scatter(stat_dict, x="Packet count", y="Time (seconds)", title=stat_dict["Title"])
        title = stat_dict["Title"]
        figure.write_image(f"{output_folder}{title}.png")


def test_packet_count():
    """
    Tests if the number of packets provided by the adapter is correct.

    Creates a new BackendAdapter object for each packet.
    """
    print("\nStarting packet count test with one BackendAdapter for each pcap file.")
    random.shuffle(test_pcap_files)
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        start_time = datetime.now()
        adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        adapter_init_time = datetime.now() - start_time
        start_time = datetime.now()
        packets = adapter.get_packet_information()
        get_packet_information_time = datetime.now() - start_time
        GET_PACKET_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        GET_PACKET_DICT["Time (seconds)"].append(get_packet_information_time.total_seconds())
        INIT_BACKEND_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        INIT_BACKEND_DICT["Time (seconds)"].append(adapter_init_time.total_seconds())
        print(f"BackendAdapter initialization time: {adapter_init_time}\nGet packet information time: {get_packet_information_time}")
        assert len(packets) == pcap_file[PACKET_COUNT]
        print(f"[{datetime.now()}]: Test passed.")


def test_packet_count_one_backend():
    """
    Tests if the number of packets provided by the adapter is correct.

    Uses only one BackendAdapter object using the BackendAdapter.update_pcap() method
    """
    print("\nStarting packet count test with one BackendAdapter.")
    adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{test_pcap_files[0][PCAP_NAME]}")
    random.shuffle(test_pcap_files)
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        start_time = datetime.now()
        adapter.update_pcap(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        update_pcap_time = datetime.now() - start_time
        start_time = datetime.now()
        packets = adapter.get_packet_information()
        get_packet_information_time = datetime.now() - start_time
        GET_PACKET_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        GET_PACKET_DICT["Time (seconds)"].append(get_packet_information_time.total_seconds())
        UPDATE_PCAP_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        UPDATE_PCAP_DICT["Time (seconds)"].append(update_pcap_time.total_seconds())
        print(f"Update pcap time: {update_pcap_time}\nGet packet information time: {get_packet_information_time}")
        assert len(packets) == pcap_file[PACKET_COUNT]
        print(f"[{datetime.now()}]: Test passed.")


def test_mac_count():
    """
    Tests if the number of MAC addresses provided by the adapter is correct.

    Creates a new BackendAdapter object for each packet.
    """
    print("\nStarting device count test with one BackendAdapter for each PCAP file.")
    random.shuffle(test_pcap_files)
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        start_time = datetime.now()
        adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        adapter_init_time = datetime.now() - start_time
        start_time = datetime.now()
        devices = adapter.get_device_macs()
        get_device_time = datetime.now() - start_time
        GET_DEVICES_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        GET_DEVICES_DICT["Time (seconds)"].append(get_device_time.total_seconds())
        INIT_BACKEND_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        INIT_BACKEND_DICT["Time (seconds)"].append(adapter_init_time.total_seconds())
        print(f"BackendAdapter initialization time: {adapter_init_time}\nGet device time: {get_device_time}")
        assert len(devices) == pcap_file[DEVICE_COUNT]
        print(f"[{datetime.now()}]: Test passed.")


def test_mac_count_one_backend():
    """
    Tests if the number of MAC addresses provided by the adapter is correct.

    Uses only one BackendAdapter object using the BackendAdapter.update_pcap() method
    """
    print("\nStarting device count test with one BackendAdapter.")
    adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{test_pcap_files[0][PCAP_NAME]}")
    random.shuffle(test_pcap_files)
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        start_time = datetime.now()
        adapter.update_pcap(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        adapter_update_time = datetime.now() - start_time
        start_time = datetime.now()
        devices = adapter.get_device_macs()
        get_device_time = datetime.now() - start_time
        GET_DEVICES_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        GET_DEVICES_DICT["Time (seconds)"].append(get_device_time.total_seconds())
        UPDATE_PCAP_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        UPDATE_PCAP_DICT["Time (seconds)"].append(adapter_update_time.total_seconds())
        print(f"Update PCAP time: {adapter_update_time}\nGet device time: {get_device_time}")
        assert len(devices) == pcap_file[DEVICE_COUNT]
        print(f"[{datetime.now()}]: Test passed.")


def test_connection_count():
    """
    Tests if the number of Connections provided by the adapter is correct.

    Creates a new BackendAdapter object for each packet.
    """
    print("\nStarting connection count test with one BackendAdapter for each PCAP file.")
    random.shuffle(test_pcap_files)
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        start_time = datetime.now()
        adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        adapter_init_time = datetime.now() - start_time
        start_time = datetime.now()
        connections = adapter.get_connections()
        get_connections_time = datetime.now() - start_time
        GET_CONNECTIONS_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        GET_CONNECTIONS_DICT["Time (seconds)"].append(get_connections_time.total_seconds())
        INIT_BACKEND_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        INIT_BACKEND_DICT["Time (seconds)"].append(adapter_init_time.total_seconds())
        print(f"BackendAdapter initialization time: {adapter_init_time}\nGet connections: {get_connections_time}")
        assert calculate_connection_count(connections) == pcap_file[CONNECTION_COUNT]
        print("Test case passed.")


def test_connection_count_one_backend():
    """
    Tests if the number of Connections provided by the adapter is correct.

    Uses only one BackendAdapter object using the BackendAdapter.update_pcap() method
    """
    print("\nStarting connection count test with one BackendAdapter.")
    adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{test_pcap_files[0][PCAP_NAME]}")
    random.shuffle(test_pcap_files)
    for pcap_file in test_pcap_files:
        print(f"[{datetime.now()}]: testing {pcap_file[PCAP_NAME]} ({pcap_file[PACKET_COUNT]} packets)...")
        start_time = datetime.now()
        adapter.update_pcap(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        adapter_update_time = datetime.now() - start_time
        start_time = datetime.now()
        connections = adapter.get_connections()
        get_connections_time = datetime.now() - start_time
        GET_CONNECTIONS_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        GET_CONNECTIONS_DICT["Time (seconds)"].append(get_connections_time.total_seconds())
        UPDATE_PCAP_DICT["Packet count"].append(pcap_file[PACKET_COUNT])
        UPDATE_PCAP_DICT["Time (seconds)"].append(adapter_update_time.total_seconds())
        print(f"BackendAdapter update time: {adapter_update_time}\nGet connections: {get_connections_time}")
        assert calculate_connection_count(connections) == pcap_file[CONNECTION_COUNT]
        print("Test case passed.")


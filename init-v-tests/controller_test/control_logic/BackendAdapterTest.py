import json
import os
import random
from datetime import datetime
from controller.init_v_controll_logic.BackendAdapter import BackendAdapter

# Define constants
RESOURCE_FOLDER_PATH = os.path.abspath(f"..{os.sep}..{os.sep}resources{os.sep}pcap files") + os.sep
PCAP_NAME = "pcap_name"
PACKET_COUNT = "packet_count"
CONNECTION_COUNT = "connection_count"
DEVICE_COUNT = "device_count"


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
        print(f"Update pcap time: {update_pcap_time}\nGet packet information time: {get_packet_information_time}")
        assert len(packets) == pcap_file[PACKET_COUNT]
        print(f"[{datetime.now()}]: Test passed.")


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
        print(f"BackendAdapter initialization time: {adapter_init_time}\nGet packet information time: {get_packet_information_time}")
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
        print(f"BackendAdapter update time: {adapter_update_time}\nGet connections: {get_connections_time}")
        assert calculate_connection_count(connections) == pcap_file[CONNECTION_COUNT]
        print("Test case passed.")


import json
import os
from controller.init_v_controll_logic.BackendAdapter import BackendAdapter

# Define constants
RESOURCE_FOLDER_PATH = os.path.abspath(f"..{os.sep}..{os.sep}resources{os.sep}pcap files") + os.sep
PCAP_NAME = "pcap_name"
PACKET_COUNT = "packet_count"
CONNECTION_COUNT = "connection_count"
DEVICE_COUNT = "device_count"


# Load resource json file for packet information
test_pcap_json_file = open(f"{RESOURCE_FOLDER_PATH}pcap_properties.json")
test_pcap_files = [pcap_file for pcap_file in json.load(test_pcap_json_file) if pcap_file[PACKET_COUNT] <= 1000]
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
    adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{test_pcap_files[0][PCAP_NAME]}")
    for pcap_file in test_pcap_files:
        print("Testing pcap file: ", pcap_file[PCAP_NAME])
        adapter.update_pcap(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        assert len(adapter.get_packet_information()) == pcap_file[PACKET_COUNT]
        print("Test case passed.")


def test_packet_count():
    """
    Tests if the number of packets provided by the adapter is correct.

    Creates a new BackendAdapter object for each packet.
    """
    for pcap_file in test_pcap_files:
        print("Testing pcap file: ", pcap_file[PCAP_NAME])
        adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        assert len(adapter.get_packet_information()) == pcap_file[PACKET_COUNT]
        print("Test case passed.")


def test_mac_count():
    """
    Tests if the number of MAC addresses provided by the adapter is correct.

    Creates a new BackendAdapter object for each packet.
    """
    for pcap_file in test_pcap_files:
        print("Testing pcap file: ", pcap_file[PCAP_NAME])
        adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        device_count = len(adapter.get_device_macs())
        assert device_count == pcap_file[DEVICE_COUNT]
        print("Test case passed.")


def test_mac_count_one_backend():
    """
    Tests if the number of MAC addresses provided by the adapter is correct.

    Uses only one BackendAdapter object using the BackendAdapter.update_pcap() method
    """
    adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{test_pcap_files[0][PCAP_NAME]}")
    for pcap_file in test_pcap_files:
        print("Testing pcap file: ", pcap_file[PCAP_NAME])
        adapter.update_pcap(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        device_count = len(adapter.get_device_macs())
        assert device_count == pcap_file[DEVICE_COUNT]
        print("Test case passed.")


def test_connection_count():
    """
    Tests if the number of Connections provided by the adapter is correct.

    Creates a new BackendAdapter object for each packet.
    """
    for pcap_file in test_pcap_files:
        print("Testing pcap file: ", pcap_file[PCAP_NAME])
        adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        assert calculate_connection_count(adapter.get_connections()) == pcap_file[CONNECTION_COUNT]
        print("Test case passed.")


def test_connection_count_one_backend():
    """
    Tests if the number of Connections provided by the adapter is correct.

    Uses only one BackendAdapter object using the BackendAdapter.update_pcap() method
    """
    adapter = BackendAdapter(f"{RESOURCE_FOLDER_PATH}{test_pcap_files[0][PCAP_NAME]}")
    for pcap_file in test_pcap_files:
        print("Testing pcap file: ", pcap_file[PCAP_NAME])
        adapter.update_pcap(f"{RESOURCE_FOLDER_PATH}{pcap_file[PCAP_NAME]}")
        assert calculate_connection_count(adapter.get_connections()) == pcap_file[CONNECTION_COUNT]
        print("Test case passed.")


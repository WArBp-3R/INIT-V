from backend.Backend import Backend
import os
import json
from datetime import datetime, timedelta

backend: Backend = Backend()

# Define constants
RESOURCE_FOLDER_PATH = f"resources{os.sep}pcap files{os.sep}"
PCAP_NAME = "pcap_name"
PACKET_COUNT = "packet_count"
CONNECTION_COUNT = "connection_count"
DEVICE_COUNT = "device_count"


# Load resource json file for packet information
print(os.path.abspath(""))
test_pcap_json_file = open(f"{RESOURCE_FOLDER_PATH}pcap_properties.json")
test_pcap_files = json.load(test_pcap_json_file)
test_pcap_json_file.close()


def calculate_all_pcap_data(max_packet_count=-1, show_time_information=False):
    if max_packet_count > 0:
        pcap_files = [pcap_file for pcap_file in test_pcap_files if pcap_file[PACKET_COUNT] <= max_packet_count]
    else:
        pcap_files = test_pcap_files
    for pcap_file in pcap_files:
        calculate_pcap_data(pcap_file[PCAP_NAME], show_time_information)


def calculate_device_count(pcap_id) -> (int, timedelta):
    start_time = datetime.now()
    macs = backend.get_macs(pcap_id)
    get_macs_time = datetime.now() - start_time
    return len(macs), get_macs_time


def calculate_connection_count(pcap_id) -> (int, timedelta):
    total_connections = 0
    start_time = datetime.now()
    connections = backend.get_connections(pcap_id)
    get_connections_time = datetime.now() - start_time
    for device, device_dict in connections.items():
        for protocol, connected_devices in device_dict.items():
            total_connections += len(connected_devices)
    return int(total_connections / 2), get_connections_time


def calculate_packet_count(pcap_id) -> (int, timedelta):
    start_time = datetime.now()
    packets = backend.get_packets(pcap_id)
    get_packet_time: timedelta = datetime.now() - start_time
    packet_count = len(packets)
    return packet_count, get_packet_time


def calculate_pcap_data(pcap_name, show_time_information=False):
    start_time = datetime.now()
    pcap_id = backend.set_pcap(os.path.abspath(f"resources\\pcap files\\{pcap_name}"))
    set_pcap_time = datetime.now() - start_time
    packet_count, packet_calculation_time = calculate_packet_count(pcap_id)
    connection_count, connection_calculation_time = calculate_connection_count(pcap_id)
    device_count, device_calculation_time = calculate_device_count(pcap_id)
    print(f"Statistics of pcap {pcap_name}:", f"Total packet count: {packet_count}",
          f"Total connection count: {connection_count}",
          f"Total device count: {device_count}",
          sep="\n")
    if show_time_information:
        print(f"get_macs time: = {device_calculation_time}", f"get_packets_time: = {packet_calculation_time}",
              f"get_connections time: {connection_calculation_time}", "", sep="\n")


def show_pcap_connections(pcap_name):
    pcap_id = backend.set_pcap(os.path.abspath(f"resources\\{pcap_name}"))
    for device, connections in backend.get_connections(pcap_id).items():
        print(f"Device {device} is connected to:")
        for protocol, connected_devices in connections.items():
            print(f"\t For the protocol {protocol}:")
            for connected_device in connected_devices:
                print(f"\t\t {connected_device}")


if __name__ == "__main__":
    calculate_all_pcap_data(show_time_information=True, max_packet_count=100000)


"""
The BackendAdapter module which contains the BackendAdapter class.
"""
import scapy.packet
from keras.callbacks import History

import logging

from backend.Backend import Backend

from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration


class BackendAdapter:
    """
    The BackendAdapter class that gets used as an intermediary between the Calculator class and the
    provided Backend.
    """

    def __init__(self, pcap_path: str):
        """
        Constructor of the BackendAdapter.
        :param pcap_path: The path of the PCAP file.
        """
        self.backend = Backend()
        self.pcap_id: str = self.backend.set_pcap(pcap_path)
        logging.debug('backend adapter initialized')

    def calculate_pca(self, config: Configuration) -> ((float, float), list):
        """
        Calculates an encoding of the packets with the PCA method.
        :param config: Configuration of the PCA.
        :return: A tuple for the performance data of the PCA method and a list of two-dimensional
        float mappings of each packet of the objects assigned pcap file.
        """
        self._configure_preprocessor(config)
        self.backend.set_parameters_pca(encoding_size=2)
        performance = self.backend.train_pca(self.pcap_id)
        float_perf = (float(performance[0]), float(performance[1]))
        packets = self.backend.encode_pca(self.pcap_id)
        logging.debug('pca calculated')
        return float_perf, packets

    def calculate_autoencoder(self, config: Configuration) -> (History, list):
        """
        Calculates an encoding of the packets with the Autoencoder method.
        :param config: Configuration of the Autoencoder.
        :return: An History object for the performance data of the Autoencoder method and a list of
        two dimensional float mappings of each packet of the objects assigned pcap file.
        """
        self._configure_preprocessor(config)
        autoencoder_config: AutoencoderConfiguration = config.autoencoder_config
        self.backend.set_parameters_autoencoder(sample_size=config.sample_size,
                                                number_of_hidden_layers=autoencoder_config
                                                .number_of_hidden_layers,
                                                nodes_of_hidden_layers=autoencoder_config
                                                .nodes_of_hidden_layers,
                                                loss=autoencoder_config.loss_function,
                                                epochs=autoencoder_config.number_of_epochs,
                                                optimizer=autoencoder_config.optimizer)
        hist: History = self.backend.train_autoencoder(self.pcap_id)
        packets: list = self.backend.encode_autoencoder(self.pcap_id)
        logging.debug('autoencoder calculated')
        return hist, packets

    def get_packet_information(self) -> list[(scapy.packet.Packet, list[str])]:
        """
        Getter of the packet and protocol of each packet of the adapter objects assigned PCAP file.
        :return: A list of tuples, the first element of the tuple is a scapy packet object, the
        second element is a list of the names of the protocols used by the packet.
        """
        packets_protocols_tuple: (list, list) = self.backend.get_packets_protocols(self.pcap_id)
        return list(zip(packets_protocols_tuple[0], packets_protocols_tuple[1]))

    def get_device_macs(self) -> list:
        """
        Getter for the mac addresses of the receiving and sending ends of the packets of the adapter
        objects assigned PCAP file.
        :return: A list of MAC addresses.
        """
        return self.backend.get_macs(self.pcap_id)

    def get_associated_ips(self, mac_address: str) -> list:
        """
        Gets associated IP addresses of a MAC address in the adapter objects assigned PCAP file.
        :param mac_address: The MAC address whose associated IP addresses is requested.
        :return: A list of IP addresses associated with the MAC address.
        """
        return self.backend.get_ips(self.pcap_id, mac_address)

    def get_connections(self) -> dict:
        """
        Returns the connections in the adapter objects pcap file as a dictionary. Details of the
        dictionary is specified in the Backend.get_connections(pcap_id) method.
        :return: A dictionary of all connections.
        """
        return self.backend.get_connections(self.pcap_id)

    def update_pcap(self, pcap_path: str):
        """
        Updates the assigned pcap of the adapter.
        :param pcap_path: Path of the pcap
        """
        self.pcap_id = self.backend.set_pcap(pcap_path)

    def _configure_preprocessor(self, config: Configuration):
        """
        Configures the preprocessor which is used before calculating with the PCA or Autoencoder
        method.
        :param config: The configuration
        """
        self.backend.set_preprocessing(normalization_method=config.normalization,
                                       scaling_method=config.scaling,
                                       sample_size=config.sample_size)
        logging.debug('preprocessor configured')
        
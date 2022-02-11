import scapy.packet

from controller.init_v_controll_logic.BackendInterface import BackendInterface
from backend.Backend import Backend
from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from keras.callbacks import History


class BackendAdapter(BackendInterface):

    def __init__(self, pcap_path: str):
        self.backend = Backend()
        self.pcap_id: str = self.backend.set_pcap(pcap_path)

    def calculate_pca(self, config: Configuration) -> ((float, float), list):
        self._configure_preprocessor(config)
        self.backend.set_parameters_pca(config.length_scaling)
        performance = self.backend.train_pca(self.pcap_id)
        packets = self.backend.encode_pca(self.pcap_id)
        return performance, packets

    def calculate_autoencoder(self, config: Configuration) -> (History, list):
        self._configure_preprocessor(config)
        autoencoder_config: AutoencoderConfiguration = config.autoencoder_config
        self.backend.set_parameters_autoencoder(number_of_hidden_layers=autoencoder_config.number_of_layers,
                                                nodes_of_hidden_layers=autoencoder_config.number_of_nodes,
                                                loss=autoencoder_config.loss_function,
                                                epochs=autoencoder_config.number_of_epochs,
                                                optimizer=autoencoder_config.optimizer)
        hist: History = self.backend.train_autoencoder(self.pcap_id)
        packets: list = self.backend.encode_autoencoder(self.pcap_id)
        return hist, packets

    def get_packet_information(self) -> list[(scapy.packet.Packet, str)]:
        def _get_highest_protocol(protocols: list[str]) -> str:
            if protocols[-1] == "Padding" or protocols[-1] == "Raw":
                return protocols[-2]
            return protocols[-1]

        packets_protocols_tuple: (list, list) = self.backend.get_packets_protocols(self.pcap_id)
        packets = packets_protocols_tuple[0]
        highest_protocols = list(map(_get_highest_protocol, packets_protocols_tuple[1]))
        return list(zip(packets, highest_protocols))

    def get_device_macs(self) -> list:
        return self.backend.get_macs(self.pcap_id)

    def get_associated_ips(self, mac_address: str) -> list:
        return self.backend.get_ips(self.pcap_id, mac_address)

    def get_connections(self) -> dict:
        return self.backend.get_connections(self.pcap_id)

    def update_pcap(self, pcap_path: str):
        self.pcap_id = self.backend.set_pcap(pcap_path)

    def _configure_preprocessor(self, config: Configuration):
        self.backend.set_preprocessing(normalization_method=config.normalization,
                                       scaling_method="ValueLength" if config.value_scaling else "Length")

from controller.init_v_controll_logic.BackendInterface import BackendInterface
from backend import Backend
from model import Configuration, AutoencoderConfiguration
from keras.callbacks import History


class BackendAdapter(BackendInterface):

    def __init__(self, pcap_path: str):
        self.backend = Backend()
        self.pcap_id = self.backend.set_pcap(pcap_path)
        self.pcap_path = pcap_path

    def calculate_pca(self, pcap_path: str, config: Configuration) -> ((float, float), list):
        self._update_pcap(pcap_path)
        self._configure_preprocessor(config)
        # TODO Configure pca
        performance = self.backend.train_pca(self.pcap_id)
        packets = self.backend.encode_pca(self.pcap_id)
        return performance, packets

    def calculate_autoencoder(self, pcap_path: str, config: Configuration) -> (History, list):
        self._update_pcap(pcap_path)
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

    def calculate_topology(self, pcap_path: str, config: Configuration):
        # TODO implementation details
        pass

    def _update_pcap(self, pcap_path: str):
        if self.pcap_path != pcap_path:
            self.pcap_id = self.backend.set_pcap(pcap_path)
            self.pcap_path = pcap_path

    def _configure_preprocessor(self, config: Configuration):
        self.backend.set_preprocessing()
        # TODO Preprocessing configurations

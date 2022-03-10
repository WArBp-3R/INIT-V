from model.AutoencoderConfiguration import AutoencoderConfiguration


class Configuration:
    """The configuration of the PCAP analyser.
    The values are used as parameters of the PCA and/or autoencoder analysis of a PCAP file."""

    def __init__(self, autoencoder: bool, pca: bool, sample_size: int, scaling: str, normalization: str,
                 autoencoder_config: AutoencoderConfiguration):
        """The constructor of the class."""
        self.autoencoder = autoencoder
        """Represents if the autoencoder analysis is enabled."""
        self.pca = pca
        """Represents if the PCA analysis is enabled."""
        self.sample_size = sample_size
        """The sample size."""
        self.scaling = scaling
        """Represents if ValueLength is the selected scaling method."""
        self.normalization = normalization
        """The normalization value."""
        self.autoencoder_config = autoencoder_config
        """The configuration of the autoencoder."""

    def is_valid(self) -> bool:
        amount_of_defined_layers = self.autoencoder_config.nodes_of_hidden_layers.__len__()
        if self.autoencoder_config.nodes_of_hidden_layers == amount_of_defined_layers:
            return True
        else:
            return False
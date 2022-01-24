from model.AutoencoderConfiguration import AutoencoderConfiguration


class Configuration:
    """The configuration of the PCAP analyser.
    The values are used as parameters of the PCA and/or autoencoder analysis of a PCAP file."""

    def __init__(self, autoencoder: bool, pca: bool, length_scaling: int, normalization: str,
                 autoencoder_config: AutoencoderConfiguration):
        """The constructor of the class."""
        self.autoencoder = autoencoder
        """Represents if the autoencoder analysis is enabled."""
        self.pca = pca
        """Represents if the PCA analysis is enabled."""
        self.length_scaling = length_scaling
        """The length scaling value."""
        self.normalization = normalization
        """The normalization value."""
        self.autoencoder_config = autoencoder_config
        """The configuration of the autoencoder."""

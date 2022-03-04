from keras.callbacks import History


class PerformanceResult:
    """The analysis of the autoencoder and/or PCA analysis of a PCAP file."""

    def __init__(self, pca: (float, float), autoencoder: dict[str, list]):
        """The constructor of the class."""
        self.pca = pca
        """The performance analysis of the PCA analysis of a PCAP file."""
        self.autoencoder = autoencoder
        """The performance analysis of the autoencoder analysis of a PCAP file."""

    def get_autoencoder(self) -> dict[str, list]:
        """Getter for the autoencoder performance."""
        return self.autoencoder

    def get_pca(self) -> (float, float):
        """Getter for the PCA performance."""
        return self.pca

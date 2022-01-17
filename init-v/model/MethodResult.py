
class MethodResult:
    """Result of an autoencoder and/or PCA analysis of a PCAP file."""

    def __init__(self, pca_result: list, autoencoder_result: list):
        """The constructor of the class."""
        self.pca_result = pca_result
        """List of points representing the PCA result."""
        self.autoencoder_result = autoencoder_result
        """List of points representing the autoencoder result."""

    def get_pca_result(self) -> list:
        """Getter of the PCA result."""
        return self.pca_result

    def get_autoencoder_result(self) -> list:
        """Getter for the autoencoder result."""
        return self.autoencoder_result

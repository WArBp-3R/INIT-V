
class MethodResult:
    """Result of an autoencoder and/or PCA analysis of a PCAP file.

        The result of both autoencoder and pca is a list of four dimensional tuples.
        First two elements is a two-dimensional float coordinate obtained by the backend, the third String
        element is information on the packet, the final element is the highest protocol of the packet."""

    def __init__(self, pca_result: list[(float, float, dict[str, str], str)],
                 autoencoder_result: list[(float, float, dict[str, str], str)]):
        """The constructor of the class."""
        self.pca_result = pca_result
        """List of points representing the PCA result."""
        self.autoencoder_result = autoencoder_result
        """List of points representing the autoencoder result."""

    def get_pca_result(self) -> list[(float, float, dict[str, str], str)]:
        """Getter of the PCA result."""
        return self.pca_result

    def get_autoencoder_result(self) -> list[(float, float, dict[str, str], str)]:
        """Getter for the autoencoder result."""
        return self.autoencoder_result

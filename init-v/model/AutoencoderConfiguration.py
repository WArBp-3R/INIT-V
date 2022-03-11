class AutoencoderConfiguration:
    """The configuration of the autoencoder analyser of a PCAP file.
    Values used to configure the autoencoder are saved in a different class,
    because of the large amount of options only used by the autoencoder (and not by PCA)."""

    def __init__(self, number_of_hidden_layers: int, nodes_of_hidden_layers: list[int], loss_function: str,
                 number_of_epochs: int,
                 optimizer: str):
        """The constructor of the class."""
        self.number_of_hidden_layers = number_of_hidden_layers
        """The number of hidden layers between the input and output layer."""
        self.nodes_of_hidden_layers = nodes_of_hidden_layers
        """The number of nodes in the hidden layers as a list."""
        self.loss_function = loss_function
        """The loss function used in the autoencoder training."""
        self.number_of_epochs = number_of_epochs
        """Number of epochs for the training."""
        self.optimizer = optimizer
        """The name of the used optimizer."""

    def is_valid(self):
        if self.number_of_hidden_layers == len(self.nodes_of_hidden_layers):
            return True
        else:
            return False

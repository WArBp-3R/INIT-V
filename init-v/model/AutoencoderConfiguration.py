class AutoencoderConfiguration:

    def __init__(self, number_of_layers: int, number_of_nodes: np.array, loss_function: str, number_of_epochs: int,
                 optimizer: str):
        self.number_of_layers = number_of_layers
        self.number_of_nodes = number_of_nodes
        self.loss_function = loss_function
        self.number_of_epochs = number_of_epochs
        self.optimizer = optimizer

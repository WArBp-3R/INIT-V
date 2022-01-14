from model.AutoencoderConfiguration import AutoencoderConfiguration


class Configuration:

    def __init__(self, autoencoder: bool, pca: bool, length_scaling: int, normalization: str,
                 autoencoder_config: AutoencoderConfiguration):
        self.autoencoder = autoencoder
        self.pca = pca
        self.length_scaling = length_scaling
        self.normalization = normalization
        self.autoencoder_config = autoencoder_config

class ExportOptions:

    def __init__(self, type: str, resolution: (int, int), introduction: bool, autoencoder_result: bool, pca_result: bool, autoencoder_performance: bool, pca_performance: bool, topology: bool, statistics: bool):
        self.type = type
        self.resolution = resolution
        self.introduction = introduction
        self.autoencoder_result = autoencoder_result
        self.pca_result = pca_result
        self.autoencoder_performance = autoencoder_performance
        self.pca_performance = pca_performance
        self.topology = topology
        self.statistics = statistics

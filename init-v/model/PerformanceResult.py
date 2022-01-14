
class PerformanceResult:

    def __init__(self, pca: list, autoencoder: History):
        self.pca = pca
        self.autoencoder = autoencoder

    def get_autoencoder(self) -> History:
        return self.autoencoder

    def get_pca(self) -> list:
        return self.pca

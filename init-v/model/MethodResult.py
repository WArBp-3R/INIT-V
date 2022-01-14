
class MethodResult:

    def __init__(self, pca_result: list, autoencoder_result: list):
        self.pca_result = pca_result
        self.autoencoder_result = autoencoder_result

    def get_pca_result(self) -> list:
        return self.pca_result

    def get_autoencoder_result(self) -> list:
        return self.autoencoder_result
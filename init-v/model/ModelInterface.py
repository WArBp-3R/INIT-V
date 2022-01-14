import numpy as np


class ModelInterface:

    def push_performance(self, pca: list, autoencoder: History):
        pass

    def push_methods(self, pca_result: list):
        pass

    def push_topology(self, topology: NetworkTopology):
        pass

    def push_statistics(self, stats: list):
        pass

    def push_configuration(self, config: Configuration):
        pass

    def compare_performance(self, pca: list, autoencoder: History, pos: np.array):
        pass

    def compare_methods(self, pca_result: list, autoencoder: list, pos: np.array):
        pass

    def compare_statistics(self, stats: list, pos: np.array):
        pass

    def compare_configuration(self, stats: list, pos: np.array):
        pass

    def update_configuration(self, config: Configuration):
        pass

    def add_runresult(self, result: RunResult):
        pass
from model_test.Configuration import Configuration
from model_test.RunResult import RunResult


def configuration_equal(c1: Configuration, c2: Configuration) -> bool:
    a1 = c1.autoencoder_config
    a2 = c2.autoencoder_config
    p1 = (c1.pca == c2.pca) and (c1.normalization == c2.normalization) and (c1.sample_size == c2.sample_size)
    p2 = (c1.autoencoder == c2.autoencoder) and (a1.optimizer == a2.optimizer)
    p3 = (a1.number_of_nodes == a2.number_of_nodes) and (a1.number_of_layers == a2.number_of_layers)
    p4 = (a1.number_of_epochs == a2.number_of_epochs) and (a1.loss_function == a2.loss_function)

    return p1 and p2 and p3 and p4


def run_result_equal(r1: RunResult, r2: RunResult) -> bool:
    t: bool = r1.timestamp == r2.timestamp
    c: bool = configuration_equal(r1.config, r2.config)
    mr1: bool = r1.result.pca_result == r2.result.pca_result
    mr2: bool = r1.result.autoencoder_result == r2.result.autoencoder_result
    a: bool = r1.analysis.pca == r2.analysis.pca and r1.analysis.autoencoder == r1.analysis.autoencoder
    return t and c and mr1 and mr2 and a


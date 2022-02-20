from model_test.Configuration import Configuration
from model_test.AutoencoderConfiguration import AutoencoderConfiguration


def test_constructor():
    auto_config: AutoencoderConfiguration = AutoencoderConfiguration(4, [256, 64, 32, 8], "MSE", 100, "adam")
    config: Configuration = Configuration(True, True, 150, "L1", auto_config)
    assert config.autoencoder
    assert config.pca
    assert config.length_scaling == 150
    assert config.normalization == "L1"
    assert config.auto_config.number_of_layers == 4
    assert config.auto_config.number_of_nodes == [256, 64, 32, 8]
    assert config.auto_config.loss_function == "MSE"
    assert config.auto_config.number_of_epochs == 100
    assert config.auto_config.optimizer == "adam"

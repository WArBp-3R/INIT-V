from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration


def test_constructor():
    auto_config: AutoencoderConfiguration = AutoencoderConfiguration(4, [256, 64, 32, 8], "MSE", 100, "adam")
    config: Configuration = Configuration(True, True, 150, "ValueLength", "L1", auto_config)
    assert config.autoencoder
    assert config.sample_size == 150
    assert config.scaling == "ValueLength"
    assert config.normalization == "L1"
    assert config.autoencoder_config.number_of_hidden_layers == 4
    assert config.autoencoder_config.nodes_of_hidden_layers == [256, 64, 32, 8]
    assert config.autoencoder_config.loss_function == "MSE"
    assert config.autoencoder_config.number_of_epochs == 100
    assert config.autoencoder_config.optimizer == "adam"

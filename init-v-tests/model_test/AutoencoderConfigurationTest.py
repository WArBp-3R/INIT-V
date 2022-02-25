from model.AutoencoderConfiguration import AutoencoderConfiguration


def test_constructor():
    auto_config: AutoencoderConfiguration = AutoencoderConfiguration(4, [256, 64, 32, 8], "MSE", 100, "adam")
    assert auto_config.number_of_layers == 4
    assert auto_config.number_of_nodes == [256, 64, 32, 8]
    assert auto_config.loss_function == "MSE"
    assert auto_config.number_of_epochs == 100
    assert auto_config.optimizer == "adam"

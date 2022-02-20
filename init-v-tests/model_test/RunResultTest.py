import datetime

from model_test.RunResult import RunResult
from model_test.Configuration import Configuration
from model_test.AutoencoderConfiguration import AutoencoderConfiguration
from model_test.MethodResult import MethodResult


def test_constructor():
    timestamp = datetime.datetime.now()
    auto_config: AutoencoderConfiguration = AutoencoderConfiguration(4, [256, 64, 32, 8], "MSE", 100, "adam")
    config: Configuration = Configuration(True, True, 150, "L1", auto_config)
    pca_result: list[(float, float, str)] = [(23.3, 10.7, "a"), (-13, 1312, "b")]
    autoencoder_result: list[(float, float, str)] = [(4019.4, -10, "c"), (3.1, 6.0, "d")]
    mr: MethodResult = MethodResult(pca_result, autoencoder_result)
    run: RunResult = RunResult(timestamp, config, mr)

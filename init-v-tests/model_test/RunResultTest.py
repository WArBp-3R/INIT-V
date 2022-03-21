import datetime
import CompareClass

from model.RunResult import RunResult
from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from model.PerformanceResult import PerformanceResult
from model.MethodResult import MethodResult


def test_constructor():
    timestamp = datetime.datetime.now()
    auto_config: AutoencoderConfiguration = AutoencoderConfiguration(4, [256, 64, 32, 8], "MSE", 100, "adam")
    config: Configuration = Configuration(True, True, 150, "ValueLength", "L1", auto_config)
    pca_result: list[(float, float, str)] = [(23.3, 10.7, "a"), (-13, 1312, "b")]
    autoencoder_result: list[(float, float, str)] = [(4019.4, -10, "c"), (3.1, 6.0, "d")]
    mr: MethodResult = MethodResult(pca_result, autoencoder_result)
    auto: dict[str, list] = {"W": [1, 65840]}
    pca: (float, float) = (13.2, -79)
    pr: PerformanceResult = PerformanceResult(pca, auto)
    run: RunResult = RunResult(timestamp, config, mr, pr)
    assert timestamp == run.timestamp
    assert config == run.config
    assert pca_result == run.result.pca_result
    assert autoencoder_result == run.result.autoencoder_result
    assert auto == run.analysis.autoencoder
    assert pca == run.analysis.pca


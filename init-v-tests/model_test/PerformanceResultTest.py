from model_test.PerformanceResult import PerformanceResult
from controller.init_v_controll_logic.Calculator import Calculator
from model_test.AutoencoderConfiguration import AutoencoderConfiguration
from model_test.Configuration import Configuration
from model_test.RunResult import RunResult


def test_constructor():
    auto_config: AutoencoderConfiguration = AutoencoderConfiguration(4, [256, 64, 32, 8], "MSE", 100, "adam")
    config: Configuration = Configuration(True, True, 150, "L1", auto_config)
    calc: Calculator = Calculator("backend/small_example.pcapng")
    run_result: RunResult = calc.calculate_run("backend/small_example.pcapng")
    pr: PerformanceResult = PerformanceResult(run_result.analysis.pca, run_result.analysis.autoencoder)
    assert pr.pca == run_result.analysis.pca
    assert pr.autoencoder == run_result.analysis.autoencoder

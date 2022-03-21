from model.PerformanceResult import PerformanceResult
from controller.init_v_controll_logic.Calculator import Calculator
from model.AutoencoderConfiguration import AutoencoderConfiguration
from model.Configuration import Configuration
from model.RunResult import RunResult


def test_constructor():
    auto: dict[str, list] = {"W": [1, 65840]}
    pca: (float, float) = (13.2, -79)
    pr: PerformanceResult = PerformanceResult(pca, auto)
    assert pca == pr.pca
    assert auto == pr.autoencoder

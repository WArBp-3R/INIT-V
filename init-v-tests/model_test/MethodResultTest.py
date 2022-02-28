from model.MethodResult import MethodResult


def test_constructor():
    pca_result: list[(float, float, str)] = [(23.3, 10.7, "a"), (-13, 1312, "b")]
    autoencoder_result: list[(float, float, str)] = [(4019.4, -10, "c"), (3.1, 6.0, "d")]
    mr: MethodResult = MethodResult(pca_result, autoencoder_result)
    assert mr.pca_result == pca_result
    assert mr.autoencoder_result == autoencoder_result


def test_get_pca_result():
    pca_result: list[(float, float, str)] = [(23.3, 10.7, "a"), (-13, 1312, "b")]
    autoencoder_result: list[(float, float, str)] = [(4019.4, -10, "c"), (3.1, 6.0, "d")]
    mr: MethodResult = MethodResult(pca_result, autoencoder_result)
    assert mr.get_pca_result() == mr.pca_result


def test_get_autoencoder_result():
    pca_result: list[(float, float, str)] = [(23.3, 10.7, "a"), (-13, 1312, "b")]
    autoencoder_result: list[(float, float, str)] = [(4019.4, -10, "c"), (3.1, 6.0, "d")]
    mr: MethodResult = MethodResult(pca_result, autoencoder_result)
    assert mr.get_autoencoder_result() == mr.autoencoder_result

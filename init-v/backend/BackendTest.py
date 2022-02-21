"""Tests for the backend. Use pytest to run it."""
from unittest import mock

from backend.Backend import Backend
from unittest.mock import MagicMock

backend_small = Backend()
backend = Backend()
backend_bug = Backend()

small_mac_one = "00:50:56:ef:02:f5"
small_mac_two = "00:0c:29:0f:94:2e"
small_pcap_id = "pcap_0"


########################################################################################################################
# Tests for API functions
########################################################################################################################


def test_set_pcap():
    assert len(backend.pcaps) == 0
    backend.set_pcap("example.pcapng")
    assert len(backend.pcaps) == 1
    assert "pcap_0" in backend.pcaps
    assert backend.pcaps["pcap_0"] == "example.pcapng"
    try:
        backend.set_pcap("not_existing_pcap.pcapng")
    except FileNotFoundError:
        assert True
    else:
        assert False


def test_get_macs():
    pcap_id = backend_small.set_pcap("small_example.pcapng")
    macs = backend_small.get_macs(pcap_id)
    assert len(macs) == 2
    assert small_mac_one in macs
    assert small_mac_two in macs
    try:
        backend_small.get_macs("this is an invalid id")
    except ValueError:
        assert True
    else:
        assert False


def test_get_ips():
    pcap_id = backend_small.set_pcap("small_example.pcapng")
    macs = backend_small.get_macs(pcap_id)
    ips_small_mac_one = backend_small.get_ips(pcap_id, small_mac_one)
    ips_small_mac_two = backend_small.get_ips(pcap_id, small_mac_two)
    assert len(ips_small_mac_one) == 2
    assert "192.168.5.2" in ips_small_mac_one
    assert "93.184.216.34" in ips_small_mac_one
    assert len(ips_small_mac_two) == 1
    assert ips_small_mac_two[0] == "192.168.5.128"


def test_get_connections():
    conns = backend_small.get_connections(small_pcap_id)
    assert len(conns) == 2
    assert small_mac_one in conns
    assert small_mac_two in conns
    assert len(conns[small_mac_one]) == len(conns[small_mac_two])
    assert "Ethernet" in conns[small_mac_one]
    assert "Ethernet" in conns[small_mac_two]
    assert "IP" in conns[small_mac_one]
    assert "IP" in conns[small_mac_two]
    assert "UDP" in conns[small_mac_one]
    assert "UDP" in conns[small_mac_two]
    assert "TCP" in conns[small_mac_one]
    assert "TCP" in conns[small_mac_two]
    assert "DNS" in conns[small_mac_one]
    assert "DNS" in conns[small_mac_two]


def test_get_packets():
    packets = backend_small.get_packets(small_pcap_id)
    assert len(packets) == 15
    assert packets[0].src == small_mac_two
    assert packets[0].dst == small_mac_one


def test_get_packets_protocols():
    packets, protocols = backend_small.get_packets_protocols(small_pcap_id)
    assert len(packets) == 15
    assert packets[0].src == small_mac_two
    assert packets[0].dst == small_mac_one
    highest_protocols = [proto[-1] for proto in protocols]
    assert highest_protocols[10] == "TCP"


def test_set_preprocessing():
    backend_small.set_preprocessing("ValueLength", "None", 150)
    assert backend.PreprocessingConfig.sample_size == 150
    assert backend.PreprocessingConfig.scaling_method == "ValueLength"
    assert backend.PreprocessingConfig.normalization_method == "None"
    try:
        backend_small.set_preprocessing("NOT EXISTING VALUE", "None")
    except ValueError:
        assert True
    else:
        assert False
    try:
        backend_small.set_preprocessing("Length", "NOT EXISTING VALUE")
    except ValueError:
        assert True
    else:
        assert False


def test_set_parameters_autoencoder():
    assert backend_small.AutencoderConfig.autoencoder is None
    backend_small.set_parameters_autoencoder(150, 2)
    assert backend_small.AutencoderConfig.autoencoder
    assert backend_small.AutencoderConfig.encoding_size == 2


def test_set_parameters_pca():
    assert backend_small.PCAConfig.pca is None
    backend_small.set_parameters_pca(2)
    assert backend_small.PCAConfig.pca
    assert backend_small.PCAConfig.encoding_size == 2


def test_train_autoencoder():
    backend_small.set_parameters_autoencoder(150, 2)
    history = backend_small.train_autoencoder("pcap_0")
    assert len(history.epoch) == 100
    assert len(history.history["loss"]) == 100
    assert len(history.history["val_loss"]) == 100


def test_train_pca():
    backend_small.set_parameters_pca(2)
    assert backend_small.PCAConfig.pca
    assert backend_small.PCAConfig.encoding_size == 2
    mae_train, mae_test = backend_small.train_pca("pcap_0")
    assert float(mae_train) < 0.4
    assert float(mae_train) > 0
    assert float(mae_test) < 0.4
    assert float(mae_test) > 0


def test_encode_pca():
    encoded_values = backend_small.encode_pca("pcap_0")
    assert len(encoded_values) == 15
    for value in encoded_values:
        assert len(value) == 2


def test_encode_autoencoder():
    encoded_values = backend_small.encode_autoencoder("pcap_0")
    assert len(encoded_values) == 15
    for value in encoded_values:
        assert len(value) == 2


def test_bug():
    pcap_id = backend_bug.set_pcap("example.pcapng")
    backend_bug.set_preprocessing("Length", "L1", 150)

    backend_bug.set_parameters_autoencoder(number_of_hidden_layers=4, nodes_of_hidden_layers=(256, 64, 32, 8),
                                           loss="MAE", epochs=100, optimizer="adam")
    backend_bug.set_parameters_pca(2)
    history = backend_bug.train_pca(pcap_id)
    encoded_values = backend_bug.encode_pca(pcap_id)
    history_ae = backend_bug.train_autoencoder(pcap_id)
    encoded_values_ae = backend_bug.encode_autoencoder(pcap_id)
    assert history is not None
    assert history_ae is not None
    assert len(encoded_values) == 543
    assert len(encoded_values_ae) == 543
    assert True


########################################################################################################################
# Tests for non-API functions
########################################################################################################################

def test_preprocess_packets():
    mock_function = MagicMock(return_value=[0.153, 0.173, 0.328])
    mock_function_one = MagicMock(return_value=[0.153, 0.173, 0.328])

    backend_small.set_preprocessing("Length", "None", 150)
    with mock.patch("backend.Backend.scale_packet_length", mock_function):
        preprocessed_packets = backend_small.preprocess_packets("pcap_0")
    mock_function.assert_called()
    assert len(preprocessed_packets) == 15

    backend_small.set_preprocessing("ValueLength", "None", 150)
    with mock.patch("backend.Backend.scale_packet_length", mock_function):
        with mock.patch("backend.Backend.scale_packet_values", mock_function_one):
            preprocessed_packets = backend_small.preprocess_packets("pcap_0")
    mock_function.assert_called()
    mock_function_one.assert_called()
    assert len(preprocessed_packets) == 15

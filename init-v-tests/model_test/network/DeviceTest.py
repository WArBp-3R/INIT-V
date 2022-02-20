from model_test.network.Device import Device


def test_constructor():
    dev: Device = Device("mac address", "ip address")
    assert dev.mac_address == "mac address"
    assert dev.ip_address == "ip address"

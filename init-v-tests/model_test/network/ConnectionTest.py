from model_test.network.Device import Device
from model_test.network.Connection import Connection


def test_constructor():
    dev_a: Device = Device("ip address a", "mac address a")
    dev_b: Device = Device("ip address b", "mac address b")
    con: Connection = Connection(dev_a, dev_b, {"TCP", "UDP"})
    assert con.first_device == dev_a
    assert con.second_device == dev_b
    assert con.protocols == {"TCP", "UDP"}

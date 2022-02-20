from model_test.network.Device import Device
from model_test.network.Connection import Connection
from model_test.network.NetworkTopology import NetworkTopology


def test_constructor():
    dev_a: Device = Device("ip address a", "mac address a")
    dev_b: Device = Device("ip address b", "mac address b")
    dev_c: Device = Device("ip address c", "mac address c")
    dev_d: Device = Device("ip address d", "mac address d")
    dev_e: Device = Device("ip address e", "mac address e")
    dev_f: Device = Device("ip address f", "mac address f")
    protocols: set[str] = {"TCP", "UDP"}
    con1: Connection = Connection(dev_a, dev_b, protocols)
    con2: Connection = Connection(dev_c, dev_d, protocols)
    con3: Connection = Connection(dev_e, dev_f, protocols)
    net_topo: NetworkTopology = NetworkTopology([dev_a, dev_b, dev_c, dev_d, dev_e, dev_f], [con1, con2, con3])
    assert net_topo.devices == [dev_a, dev_b, dev_c, dev_d, dev_e, dev_f]
    assert net_topo.connections == [con1, con2, con3]

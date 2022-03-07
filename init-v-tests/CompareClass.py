from model.Configuration import Configuration
from model.RunResult import RunResult
from model.Session import Session
from model.network.NetworkTopology import NetworkTopology
from model.MethodResult import MethodResult
from model.PerformanceResult import PerformanceResult
from model.network.Device import Device
from model.network.Connection import Connection

debug = False  # set to True if tests fail


def configuration_equal(c1: Configuration, c2: Configuration) -> bool:
    a1 = c1.autoencoder_config
    a2 = c2.autoencoder_config
    p1 = (c1.pca == c2.pca) and (c1.normalization == c2.normalization) and (c1.sample_size == c2.sample_size)
    p2 = (c1.autoencoder == c2.autoencoder) and (a1.optimizer == a2.optimizer)
    p3 = (a1.nodes_of_hidden_layers == a2.nodes_of_hidden_layers) and \
         (a1.number_of_hidden_layers == a2.number_of_hidden_layers)
    p4 = (a1.number_of_epochs == a2.number_of_epochs) and (a1.loss_function == a2.loss_function)
    if debug:
        print('sample_size equal: ' + (c1.sample_size == c2.sample_size).__str__() + '\n')
    return p1 and p2 and p3 and p4


def run_result_equal(r1: RunResult, r2: RunResult) -> bool:
    t: bool = r1.timestamp == r2.timestamp
    c: bool = configuration_equal(r1.config, r2.config)
    mr: bool = method_result_equal(r1.result, r2.result)
    a: bool = performance_result_equal(r1.analysis, r2.analysis)
    if debug:
        print('timestamp equal?: ' + t.__str__() + '\n')
        print('config equal?: ' + c.__str__() + '\n')
        print('method equal?: ' + mr.__str__() + '\n')
        print('performance equal?: ' + a.__str__() + '\n')
    return t and c and mr and a


def topology_equal(t1: NetworkTopology, t2: NetworkTopology) -> bool:
    if len(t1.devices) != len(t2.devices) or len(t1.connections) != len(t2.connections):
        return False

    for i in range(len(t1.devices)):
        if not device_equal(t1.devices[i], t2.devices[i]):
            return False

    for i in range(len(t1.connections)):
        if not connection_equal(t1.connections[i], t2.connections[i]):
            return False

    return True


def connection_equal(c1: Connection, c2: Connection) -> bool:
    return device_equal(c1.first_device, c2.first_device) and c1.protocols == c2.protocols and \
           device_equal(c1.second_device, c2.second_device)


def device_equal(d1: Device, d2: Device) -> bool:
    return d1.mac_address == d2.mac_address


def performance_result_equal(pr1: PerformanceResult, pr2: PerformanceResult) -> bool:
    pca_equal = pr1.pca == pr2.pca
    autoencoder_equal = len(pr1.autoencoder) == len(pr2.autoencoder)
    if debug:
        print('autoencoder_equal: ' + autoencoder_equal.__str__() + '\n')
        print('pca_equal: ' + pca_equal.__str__() + '\n')
    return pca_equal and autoencoder_equal


def method_result_equal(m1: MethodResult, m2: MethodResult) -> bool:
    return m1.pca_result == m2.pca_result and m1.autoencoder_result == m2.autoencoder_result


def session_equal(s1: Session, s2: Session) -> bool:
    # pp: bool = s1.PCAP_PATH == s2.PCAP_PATH
    protocols: bool = s1.protocols == s2.protocols
    h_protocols: bool = len(s1.highest_protocols) == len(s2.highest_protocols)
    rrs: bool = True
    if len(s1.run_results) != len(s2.run_results):
        if debug:
            print('different number of runs\n')
        return False
    for i in range(len(s1.run_results)):
        if not run_result_equal(s1.run_results[i], s2.run_results[i]):
            if debug:
                print('run number ' + i.__str__() + ' is not equal\n')
            return False
    config: bool = configuration_equal(s1.active_config, s2.active_config)
    topology: bool = topology_equal(s1.topology, s2.topology)
    if debug:
        print('----Equal?----\n')
        # print('pp: ' + pp.__str__() + '\n')
        # if not pp:
        #    print('Path1: ' + s1.PCAP_PATH + ' Path2: ' + s2.PCAP_PATH)
        print('protocols: ' + protocols.__str__() + '\n')
        print('h_protocols: ' + h_protocols.__str__() + '\n')
        print('rrs: ' + rrs.__str__() + '\n')
        print('config: ' + config.__str__() + '\n')
        print('topology: ' + topology.__str__() + '\n')
    return protocols and h_protocols and rrs and config and topology

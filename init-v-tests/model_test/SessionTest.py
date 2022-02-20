import RandCreator
from model_test.RunResult import RunResult
from model_test.Configuration import Configuration
from model_test.network.NetworkTopology import NetworkTopology
from model_test.Session import Session
import CompareClass


def test():
    PCAP_PATH: str = "packets.pcapng"
    protocols: set[str] = {"TCP", "UDP"}
    run_results: list[RunResult] = []
    i = 0
    while i < 5:
        run_results.append(RandCreator.create_rand_run_result(10))
        i = i + 1
    active_config: Configuration = RandCreator.create_rand_config()
    topology: NetworkTopology = RandCreator.create_rand_network_topology(2, 10, {"TCP"})
    session: Session = Session(PCAP_PATH, protocols, run_results, active_config, topology, None)
    assert session.PCAP_PATH == PCAP_PATH
    assert session.protocols == protocols
    i = 0
    while i < 5:
        assert CompareClass.run_result_equal(session.run_results[i], run_results[i])
    assert CompareClass.configuration_equal(active_config, session.active_config)

    rr: RunResult = RandCreator.create_rand_run_result(10)
    session.add_run_result(rr)
    assert CompareClass.run_result_equal(rr, session.run_results[-1])

    n_config: Configuration = RandCreator.create_rand_config()
    session.update_configuration(n_config)
    assert CompareClass.configuration_equal(n_config, session.active_config)





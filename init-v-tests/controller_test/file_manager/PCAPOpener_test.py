from controller.file_manager.PCAPOpener import PCAPOpener
import RandCreator
import CompareClass

test_pcap_path = ''
config = RandCreator.create_rand_config()


def test_load_pcap():
    pc = PCAPOpener()
    session = pc.load_pcap(test_pcap_path, config)
    s_config = session.active_config
    assert(CompareClass.configuration_equal(config, s_config))

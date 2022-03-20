import pathlib
import shutil

import pytest
import os
from controller.init_v_controll_logic.Controller import Controller

import RandCreator
import CompareClass

from model.Session import Session
from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from model.RunResult import RunResult
from model.MethodResult import MethodResult
from model.PerformanceResult import PerformanceResult
from model.Statistics import Statistics

PCAP_PATH = os.getcwd() + os.sep + "resources" + os.sep + "pcap files" + os.sep + "small_example.pcapng"
RANDOM_SESSION = RandCreator.create_rand_session(0, 0, 0, 0, 0)
CONTROLLER = Controller(None, None)

BAD_CONFIG = Configuration(True, True, 100, "Length", "L1", AutoencoderConfiguration(2, [-3], "MSE", 20, "adam"))
VALID_CONFIG = Configuration(True, True, 100, "Length", "L1", AutoencoderConfiguration(2, [2 , 4], "MSE", 20, "adam"))

def setup_module():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    CONTROLLER = Controller(RANDOM_SESSION, None)

def test___init__():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)

    assert (CompareClass.session_equal(controller.session, RANDOM_SESSION) is True)
    assert (controller.calculator is not None)
    assert (controller.fileManager is not None)
    assert (controller.settings is not None)
    assert (controller.view is not None)

    controller = Controller(None, None)
    assert (controller.calculator is None)
    assert (controller.session is None)

def test__generate_directories():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)

    path = os.getcwd() + os.sep + "test"
    controller._generate_directories(path)
    assert (os.path.isdir(path + os.sep + "DEFAULT_SETTINGS"))
    assert (os.path.isdir(path + os.sep + "Configurations"))
    assert (os.path.isdir(path + os.sep + "Saves"))

    # with pytest.raises(Exception):
    #     controller._generate_directories(path)

    shutil.rmtree(pathlib.Path(path), ignore_errors=True)

def test_create_run():

    #check asserts with actuall implementation.
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)
    assert (controller.create_run(BAD_CONFIG) == 0)
    assert (controller.create_run(VALID_CONFIG) == -1)


def test_compare_runs():

    result1 = RandCreator.create_rand_run_result(0)
    result2 = RandCreator.create_rand_run_result(0)
    result3 = RandCreator.create_rand_run_result(0)

    while (CompareClass.run_result_equal(result1, result2) and CompareClass.run_result_equal(result1, result3)):
        result1 = RandCreator.create_rand_run_result(0)
        result2 = RandCreator.create_rand_run_result(0)
        result3 = RandCreator.create_rand_run_result(0)
    session = Session(PCAP_PATH, None, None, [result1, result2, result3], None, None, None)
    controller = Controller(session, None)

    runs1 = controller.compare_runs([0, 1])
    runs2 = controller.compare_runs([0, 2])
    assert(CompareClass.run_result_equal(runs1[0], runs1[1]) is False)
    assert(CompareClass.run_result_equal(runs2[0], runs2[1]) is False)


def test_get_pcap_name():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)
    assert (controller.get_pcap_name() == "small_example")

def test_update_config():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)
    controller.update_config(VALID_CONFIG)
    assert (CompareClass.configuration_equal(controller.session.active_config, VALID_CONFIG) is True)

def test_get_active_config():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)
    controller.session.active_config = VALID_CONFIG
    r_config = controller.get_active_config()
    assert (CompareClass.configuration_equal(r_config, VALID_CONFIG) is True)

def test_get_set_default_config():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)
    default_config = controller.get_default_config()
    with pytest.raises(AttributeError):
        controller.set_default_config(BAD_CONFIG)
    controller.set_default_config(VALID_CONFIG)
    assert (CompareClass.configuration_equal(controller.get_default_config(), VALID_CONFIG) is True)
    controller.set_default_config(default_config)

def test_get_run_list():

    result1 = RandCreator.create_rand_run_result(0)
    result2 = RandCreator.create_rand_run_result(0)
    result3 = RandCreator.create_rand_run_result(0)

    while (CompareClass.run_result_equal(result1, result2) and CompareClass.run_result_equal(result1, result3)):
        result1 = RandCreator.create_rand_run_result(0)
        result2 = RandCreator.create_rand_run_result(0)
        result3 = RandCreator.create_rand_run_result(0)
    session = Session(PCAP_PATH, None, None, [result1, result2, result3], None, None, None)
    controller = Controller(session, None)

    runs = controller.get_run_list()
    assert (CompareClass.run_result_equal(result1, runs[0]))
    assert (CompareClass.run_result_equal(result2, runs[1]))
    assert (CompareClass.run_result_equal(result3, runs[2]))

def test_get_network_topology():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)

    topology = RandCreator.create_rand_network_topology(0, 0, ["TCP", "UDP"])
    controller.session.topology = topology
    assert (CompareClass.topology_equal(controller.get_network_topology(), topology) is True)

def test_get_highest_protocols():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)

    highest_protocols =["TCP", "test", "test2"]
    controller.session.highest_protocols = highest_protocols
    returned_highest_protocols = controller.get_highest_protocols()
    assert (highest_protocols[0] is returned_highest_protocols [0])
    assert (highest_protocols[1] is returned_highest_protocols [1])
    assert (highest_protocols[2] is returned_highest_protocols [2])

def test_get_statistics():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)

    assert (RANDOM_SESSION.statistics is controller.session.statistics)

def test_create_new_session():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)
    controller.session.pcap_path = ""

    controller.create_new_session(PCAP_PATH)

    assert (controller.session.pcap_path is PCAP_PATH)

def test_save_and_load_config():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    controller = Controller(RANDOM_SESSION, None)
    save_path = os.getcwd() + os.sep + "test.csv"

    controller.session.active_config = BAD_CONFIG
    with pytest.raises(AttributeError):
        controller.save_config(save_path, None)

    controller.session.active_config = VALID_CONFIG
    controller.save_config(save_path, None)
    assert (os.path.exists(save_path))

    loaded_config = controller.load_config(save_path)
    assert (CompareClass.configuration_equal(loaded_config, VALID_CONFIG))

    os.remove(save_path)

def test_save_and_load_and_get_session():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    RANDOM_SESSION.active_config = VALID_CONFIG
    controller = Controller(RANDOM_SESSION, None)

    saves_path = os.getcwd() + os.sep + "test_session"
    controller.save_session(saves_path, None)
    assert (os.path.exists(saves_path) is True)

    loaded_session = controller.load_session(saves_path)
    assert (CompareClass.session_equal(loaded_session, RANDOM_SESSION) is True)

    assert (CompareClass.session_equal(controller.get_session(), RANDOM_SESSION) is True)

    shutil.rmtree(pathlib.Path(saves_path), ignore_errors=True)

def test_load_topology_graph():
    RANDOM_SESSION.pcap_path = PCAP_PATH
    RANDOM_SESSION.active_config = VALID_CONFIG
    topology = RandCreator.create_rand_network_topology(0, 0, ["TCP", "UDP"])

    pass


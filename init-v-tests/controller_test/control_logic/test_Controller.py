import pytest
from controller.init_v_controll_logic.Controller import Controller

import RandCreator

from model.Session import Session
from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from model.RunResult import RunResult
from model.MethodResult import MethodResult
from model.PerformanceResult import PerformanceResult
from model.Statistics import Statistics

RANDOM_SESSION = RandCreator.create_rand_session(0, 0, 0, 0, 0)

BAD_CONFIG = Configuration(True, True, 100, "Length", "L1", AutoencoderConfiguration(2, [-3], "MSE", 20, "adam"))
VALID_CONFIG = Configuration(True, True, 100, "Length", "L1", AutoencoderConfiguration(2, [2 , 4], "MSE", 20, "adam"))



def test_create_run():
    controller = Controller(None, None)
    #check asserts with actuall implementation.
    assert controller.create_run(BAD_CONFIG) == 1
    assert controller.create_run(VALID_CONFIG) == 0


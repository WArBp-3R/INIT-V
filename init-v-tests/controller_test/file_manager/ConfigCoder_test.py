import os

import RandCreator
import CompareClass
from controller.file_manager.ConfigEncoder import ConfigEncoder
from controller.file_manager.ConfigDecoder import ConfigDecoder

test_path = os.getcwd() + os.sep
ce = ConfigEncoder()
cd = ConfigDecoder()

# TODO add test path, change filename


def test_load_configuration():
    filename = '' + os.sep + 'load_config_test_file_name_variable_value.csv'
    c = RandCreator.create_rand_config()
    ce.save(test_path+filename, c)
    loaded = cd.load_configuration(test_path + filename)
    assert(CompareClass.configuration_equal(c, loaded))

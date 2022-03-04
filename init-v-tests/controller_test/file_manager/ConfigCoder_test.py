import os

import RandCreator
import CompareClass
from controller.file_manager.ConfigEncoder import ConfigEncoder
from controller.file_manager.ConfigDecoder import ConfigDecoder

try:
    os.mkdir(os.getcwd() + os.sep + 'test_dir')
except OSError:
    # TODO add error handling
    pass

test_path = os.getcwd() + os.sep + 'test_dir' + os.sep
ce = ConfigEncoder()
cd = ConfigDecoder()

# TODO add test path, change filename


def test_load_configuration():
    filename = 'load_config_test_file_name_variable_value.csv'
    c = RandCreator.create_rand_config()
    ce.save(test_path+filename, c)
    loaded = cd.load_configuration(test_path + filename)
    assert(CompareClass.configuration_equal(c, loaded))

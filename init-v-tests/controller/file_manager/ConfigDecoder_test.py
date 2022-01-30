import RandCreator
import CompareClass

from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from controller.file_manager.ConfigDecoder import ConfigDecoder

test_path = ''
#TODO add test path

def test_load_configuration():
    filename = 'load_config_test_file_name_variable_value'
    c = RandCreator.create_rand_config()
    #TODO save config
    loaded = ConfigDecoder.load_configuration(test_path + filename)
    assert(CompareClass.configuration_equal(c, loaded))



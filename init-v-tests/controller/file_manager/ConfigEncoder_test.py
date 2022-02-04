import RandCreator
import CompareClass
from controller.file_manager.ConfigDecoder import ConfigDecoder
from controller.file_manager.ConfigEncoder import ConfigEncoder

test_path = ''


# TODO add test path, change filename

def test_save():
    filename = 'load_config_test_file_name_variable_value'
    c = RandCreator.create_rand_config()
    ConfigEncoder.save(test_path + filename, c)
    loaded = ConfigDecoder.load_configuration(test_path + filename)
    assert (CompareClass.configuration_equal(c, loaded))

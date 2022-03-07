from controller.file_manager.FileManager import FileManager
import RandCreator
import CompareClass
import os
import shutil

fm = FileManager()
test_path = os.getcwd() + os.sep + 'test_dir' + os.sep


def test_save_load():
    saved_config = RandCreator.create_rand_config()
    saved_session = RandCreator.create_rand_session(0, 0, 0, 0, 0)
    try:
        shutil.rmtree(test_path + 'test_session_FM')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    fm.save(test_path + 'test_config_FM.csv', saved_config)
    fm.save(test_path + 'test_session_FM', saved_session, None)
    loaded_config = fm.load(test_path + 'test_config_FM.csv', 'c')
    loaded_session = fm.load(test_path + 'test_session_FM', 's')
    assert (CompareClass.configuration_equal(saved_config, loaded_config))
    assert (CompareClass.session_equal(saved_session, loaded_session))

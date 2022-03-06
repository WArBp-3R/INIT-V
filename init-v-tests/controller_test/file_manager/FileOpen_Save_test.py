import os
import shutil

from controller.file_manager.FileOpener import FileOpener
from controller.file_manager.FileSaver import FileSaver

import RandCreator
import CompareClass

test_path = os.getcwd() + os.sep + 'test_dir'
fs = FileSaver()
fo = FileOpener()


def test_open_save():
    saved_config = RandCreator.create_rand_config()
    saved_session = RandCreator.create_rand_session(0, 0, 0, 0, 0)
    try:
        shutil.rmtree(test_path + os.sep + 'session_FOS')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    fs.save(test_path + os.sep + 'test_config_FOS.csv', saved_config)
    fs.save(test_path + os.sep + 'session_FOS', saved_session, None)
    loaded_config = fo.load(test_path + os.sep + 'test_config_FOS.csv', 'c')
    loaded_session = fo.load(test_path + os.sep + 'session_FOS', 's')
    assert(CompareClass.configuration_equal(saved_config, loaded_config))
    assert(CompareClass.session_equal(saved_session, loaded_session))

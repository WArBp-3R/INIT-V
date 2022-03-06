import os
import sys
import shutil

from controller.file_manager.SessionDecoder import SessionDecoder
from controller.file_manager.SessionEncoder import SessionEncoder
import CompareClass
import RandCreator

try:
    os.mkdir(os.getcwd() + os.sep + 'test_dir')
except OSError:
    # TODO add error handling
    pass

test_path = os.getcwd() + os.sep + 'test_dir' + os.sep

se = SessionEncoder()
sd = SessionDecoder()


def test_session_coder():
    saved = RandCreator.create_rand_session(0, 0, 0, 0, 0)
    try:
        shutil.rmtree(test_path + 'test_session')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    se.save(test_path + 'test_session', saved, None)
    loaded = sd.load_session(test_path + 'test_session')
    assert CompareClass.session_equal(saved, loaded)

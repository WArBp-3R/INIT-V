import os

from controller.file_manager.SessionDecoder import SessionDecoder
from controller.file_manager.SessionEncoder import SessionEncoder
import CompareClass
import RandCreator

test_path = os.getcwd()

def test_session_coder():
    saved = RandCreator.create_rand_session(0, 0, 0, 0, 0)
    SessionEncoder.save(test_path + os.sep + 'test_dir' + os.sep + 'test_session', saved, None)
    loaded = SessionDecoder.load_session(test_path + os.sep + 'test_dir' + os.sep + 'test_session')
    assert CompareClass.session_equal(saved, loaded)

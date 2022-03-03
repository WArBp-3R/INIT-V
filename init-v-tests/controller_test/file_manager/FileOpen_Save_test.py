from model.Configuration import Configuration
from model.Session import Session

import os

from controller.file_manager.FileOpener import FileOpener
from controller.file_manager.FileSaver import FileSaver

import RandCreator

test_path = os.getcwd()


def test_open_save():
    savedConfig = RandCreator.create_rand_config()
    savedSession = RandCreator.create_rand_session(0, 0, 0, 0, 0)
    FileSaver.save(test_path + os.sep + 'test_config_FOS.csv')
    FileSaver.save(test_path + os.sep + 'session_FOS')
    loadedConfig = FileOpener.load(test_path + os.sep + 'test_config_FOS.csv', 'c')
    loadedSession = FileOpener.load

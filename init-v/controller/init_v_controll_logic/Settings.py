import os
from model.Configuration import Configuration
from controller.init_v_controll_logic.ExportOptions import ExportOptions
from controller.file_manager.FileManager import FileManager

class Settings:
    # DEFAULT_CONFIGURATION : Configuration
    # PATH : str
    # DEFAULT_EXPORT_OPTIONS : ExportOptions
    # darkMode : bool

    # TODO check
    def __init__(self, WORKSPACE_PATH: str):
        f = FileManager()
        self.DEFAULT_CONFIGURATION_PATH = WORKSPACE_PATH + os.sep + "DEFAULT_SETTINGS" + os.sep + "DEFAULT_CONFIGURATION.csv"
        self.DEFAULT_CONFIGURATION = f.load(self.DEFAULT_CONFIGURATION_PATH, "c")
        self.WORKSPACE_PATH = WORKSPACE_PATH

    def set_default_config(self, config: Configuration):
        self.DEFAULT_CONFIGURATION = config
        FileManager().save(self.DEFAULT_CONFIGURATION_PATH, config)

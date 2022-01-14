class Settings:
    DEFAULT_CONFIGURATION : Configuration
    PATH : str
    DEFAULT_EXPORT_OPTIONS : ExportOptions
    darkMode : bool

    #TODO check
    def __init__(self, WORKSPACE_PATH : str):
        self.WORKSPACE_PATH = WORKSPACE_PATH

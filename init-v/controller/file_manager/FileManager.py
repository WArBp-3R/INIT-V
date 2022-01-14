from controller.file_manager.FileManagerInterface import FileManagerInterface


class FileManager(FileManagerInterface):
    def load(self, source_path: str, option: str) -> Configuration:
        #TODO implement
        pass

    def load(self, source_path: str, option: str) -> Session:
        #TODO implement
        pass

    def save(self, output_path: str, session: Session):
        #TODO implement
        pass

    def save(self, output_path: str, config: Configuration):
        #TODO implement
        pass

    def export(self, output_path: str, session: Session, options: ExportOptions):
        #TODO implement
        pass

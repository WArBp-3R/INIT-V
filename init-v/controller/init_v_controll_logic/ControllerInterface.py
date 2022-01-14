class ControllerInterface:
    def startup(self):
        #TODO comment
        pass

    def update_topology(self):
        #TODO comment
        pass

    def create_run(self):
        #TODO comment
        pass

    def update_config(self, config: Configuration):
        #TODO comment
        pass

    def create_new_session(self, session: Session):
        #TODO comment
        pass

        
        
    def compare_runs(self, pos:int[]):
        #TODO comment
        pass

    def load_session(self, source_path: str):
        #TODO comment
        pass

    def load_config(self, source_path: str):
        #TODO comment
        pass

    def save_session(self, output_path: str):
        #TODO comment
        pass

    def save_config(self, output_path: str):
        #TODO comment
        pass

    def export(self, output_path: str, options: ExportOptions):
        #TODO comment
        pass


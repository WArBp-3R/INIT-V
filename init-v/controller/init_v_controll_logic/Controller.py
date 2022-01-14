from controller.init_v_controll_logic.ControllerInterface import ControllerInterface


class Controller (ControllerInterface):
    WORKSPACE_PATH: str
    # session: Session
    # settings: Settings

    def __init__(self, session: Session, settings: Settings):
        self.session = session
        self.settings = settings


    def startup(self):
        #TODO implement
        pass

    def update_topology(self):
        #TODO implement
        pass

    def create_run(self):
        #TODO implement
        pass

    def update_config(self, config: Configuration):
        #TODO implement
        pass

    def create_new_session(self, session: Session):
        # TODO implement
        pass



    def compare_runs(self, pos : list[int]):
        #TODO implement
        pass

    def load_session(self, source_path: str):
        #TODO implement
        pass

    def load_config(self, source_path: str):
        #TODO implement
        pass

    def save_session(self, output_path: str):
        #TODO implement
        pass

    def save_config(self, output_path: str):
        #TODO implement
        pass

    def export(self, output_path: str, options: ExportOptions):
        #TODO implement
        pass


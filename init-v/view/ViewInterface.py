from controller.init_v_controll_logic import ExportOptions


class ViewInterface:

    def create_view(self, communicator):
        pass

    def get_run_list(self) -> list:
        pass

    def create_run(self, lsc: int, vsc: list[str], nrm: str, mtd: list[str], hly: int, nhl: str, lsf: str, epc: int,
                   opt: str):
        pass

    def get_network_topology(self):
        pass

    def get_protocol_set(self) -> set[str]:
        pass

    def compare_runs(self, pos: list):
        pass

    def load_session(self, source_path: str):
        pass

    def load_config(self, source_path: str):
        pass

    def save_session(self, output_path: str, lsc: int, vsc: list[str], nrm: str, mtd: list[str], hly: int, nhl: str,
                     lsf: str, epc: int, opt: str):
        pass

    def save_config(self, output_path: str, lsc: int, vsc: list[str], nrm: str, mtd: list[str], hly: int, nhl: str,
                    lsf: str, epc: int, opt: str):
        pass

    def export(self, output_path: str, options: ExportOptions):
        pass

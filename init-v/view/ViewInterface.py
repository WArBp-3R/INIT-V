from model.network.NetworkTopology import NetworkTopology
from model import Configuration
from controller.init_v_controll_logic import ExportOptions
from keras.callbacks import History
from model.IStatistic import IStatistic
from datetime import datetime


class ViewInterface:

    def create_view(self, communicator):
        pass

    def get_run_list(self) -> list:
        pass

    def create_run(self, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        pass

    def compare_runs(self, pos: list):
        pass

    def load_session(self, source_path: str):
        pass

    def load_config(self, source_path: str):
        pass

    def save_session(self, output_path: str, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        pass

    def save_config(self, output_path: str, lsc, vsc, nrm, mtd, hly, nhl, lsf, epc, opt):
        pass

    def export(self, output_path: str, options: ExportOptions):
        pass

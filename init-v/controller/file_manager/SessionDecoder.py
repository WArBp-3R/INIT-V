import os
import pickle

from model.Session import Session
from model.RunResult import RunResult
from model.network.NetworkTopology import NetworkTopology

from controller.file_manager.ConfigDecoder import ConfigDecoder
class SessionDecoder:
    def load_session(self, source_path: str) -> Session:
        #TODO test

        #creates PCAP Path
        pcap = source_path + "\\PCAP"

        #loades the active configuration
        decoder = ConfigDecoder()
        active_config = decoder.load_configuration(source_path + "\\active_configuration.csv")

        #loades the topology
        topology = NetworkTopology(None, None)
        with open(source_path + "\\Topology", mode='rb') as topology:
            topology = pickle.load(topology)

        #loades all runs in a list
        run_list = []
        runs_path = [f.path for f in os.scandir(source_path) if f.is_dir()]
        for path in runs_path:
            if path.startswith(source_path + '\\run_' ):
                with open(path + "\\Run_Results", mode='rb') as run_result:
                    run = pickle.load(run_result)
                    run_list.append(run)

        #creates the session and returns it
        session = Session(pcap, None, run_list, active_config, topology, None)
        return session
        pass
import os
import pickle
import csv

import dash_cytoscape as cyto

from model.Session import Session
from model.RunResult import RunResult
from model.network.NetworkTopology import NetworkTopology

from controller.file_manager.ConfigDecoder import ConfigDecoder
class SessionDecoder:
    def load_session(self, source_path: str) -> Session:
        """
        method to load a session back from the disk.

        :param source_path: string of the path to the session.
        """
        # TODO test

        # creates PCAP Path
        pcap = source_path + os.sep + "PCAP.pcapng"

        # loades the active configuration
        decoder = ConfigDecoder()
        active_config = decoder.load_configuration(source_path + os.sep + "active_configuration.csv")

        # loades the topology
        topology = NetworkTopology(None, None)
        with open(source_path + os.sep + "Topology", mode='rb') as topology:
            topology = pickle.load(topology)

        # load the set of protocols
        protocols: set[str] = set()
        with open(source_path + os.sep + "list_of_protocols.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                protocols.add(row[0])

        # load the set of highest protocols
        highest_protocols: set[str] = set()
        with open(source_path + os.sep + "list_of_highest_protocols.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                highest_protocols.add(row[0])

        # loades all runs in a list
        run_list = []
        runs_path = [f.path for f in os.scandir(source_path) if f.is_dir()]
        for path in runs_path:
            if path.startswith(source_path + os.sep + 'run_'):
                if os.path.getsize(path + os.sep + "Run_Results") > 0:
                    with open(path + os.sep + "Run_Results", mode='rb') as run_result:
                        run = pickle.load(run_result)
                        run_list.append(run)

        #creates the session and returns it
        session = Session(pcap, protocols, highest_protocols, run_list, active_config, topology, None)
        return session
        pass

    def load_t_graph(self, source_path: str) -> cyto.Cytoscape:
        #TODO test
        with open(source_path+ os.sep + "Topology_graph", mode='rb') as topology_g:
            topology_g = pickle.load(topology_g)
        return topology_g
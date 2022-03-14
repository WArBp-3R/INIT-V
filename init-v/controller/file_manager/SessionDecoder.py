import os
import pickle
import csv

import dash_cytoscape as cyto

from model.Session import Session
from model.network.NetworkTopology import NetworkTopology
from controller.file_manager.ConfigDecoder import ConfigDecoder

import logging


class SessionDecoder:

    def load_session(self, source_path: str) -> Session:
        """
        method to load a session back from the disk.
        :param source_path: string of the path to the session.
        """
        # TODO test

        # creates PCAP Path
        pcap = source_path + os.sep + "PCAP.pcapng"

        # loads the active configuration
        decoder = ConfigDecoder()
        active_config = decoder.load_configuration(source_path + os.sep + "active_configuration.csv")
        logging.debug('active config loaded')

        # loads the topology
        topology: NetworkTopology
        with open(source_path + os.sep + "Topology", mode='rb') as topology:
            topology = pickle.load(topology)
        logging.debug('topology loaded')

        with open(source_path + os.sep + "statistics", mode='rb') as stats_file:
            statistics = pickle.load(stats_file)
        logging.debug('statistics loaded')

        # load the set of protocols
        protocols: set[str] = set()
        with open(source_path + os.sep + "list_of_protocols.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                protocols.add(row[0])
        logging.debug('set of protocols loaded')

        # load the set of highest protocols
        highest_protocols: set[str] = set()
        with open(source_path + os.sep + "list_of_highest_protocols.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                highest_protocols.add(row[0])
        logging.debug('set of highest protocols loaded')

        # loades all runs in a list
        run_list = []
        runs_path = [f.path for f in os.scandir(source_path) if f.is_dir()]
        for path in runs_path:
            if path.startswith(source_path + os.sep + 'run_'):
                if os.path.getsize(path + os.sep + "Run_Results") > 0:
                    with open(path + os.sep + "Run_Results", mode='rb') as run_result:
                        run = pickle.load(run_result)
                        run_list.append(run)
        logging.debug('runs loaded')

        # creates the session and returns it
        session = Session(pcap, protocols, highest_protocols, run_list, active_config, topology, statistics)
        return session
        pass

    def load_t_graph(self, source_path: str) -> cyto.Cytoscape:
        """
        loads the topology graph
        :param source_path: path from wich to load
        :return: topology as cytoscape object
        """
        # TODO test
        with open(source_path + os.sep + "Topology_graph", mode='rb') as topology_g:
            topology_g = pickle.load(topology_g)
        return topology_g

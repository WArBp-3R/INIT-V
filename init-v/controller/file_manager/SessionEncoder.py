import csv
import os
from shutil import copyfile
import pickle
import dash_cytoscape as cyto

from controller.file_manager.ConfigEncoder import ConfigEncoder
from model.Session import Session

import logging


class SessionEncoder:

    def save(self, output_path: str, session: Session, topology_graph: cyto.Cytoscape):
        """
        method will write data of a session on the disk.
        :param topology_graph: cyto.Cytoscape, topology to save
        :param  output_path: string containing the path to the output (path || name).
        :param session: Session object to be written to disk.
        """

        try:
            os.makedirs(output_path)
        except OSError as err:
            logging.error('Session encoder error: ' + str(err))
            # TODO add error handling
            pass

        # copies Pcap in session folder
        if os.path.abspath(session.pcap_path) != os.path.abspath(f"{output_path}{os.sep}PCAP.pcapng"):
            copyfile(session.pcap_path, output_path + os.sep + "PCAP.pcapng")

        # saves active configuration in session folder
        config_path = output_path + os.sep + "active_configuration.csv"
        config_encoder = ConfigEncoder()
        config_encoder.save(config_path, session.active_config)

        # saves topology in session folder
        with open(output_path + os.sep + "Topology", mode='wb') as topology:
            pickle.dump(session.topology, topology)
        logging.debug('topology saved')

        # saves topology_graph in session folder
        with open(output_path + os.sep + "Topology_graph", mode='wb') as topology_g_file:
            pickle.dump(topology_graph, topology_g_file)
        logging.debug('topology graph saved')

        with open(output_path + os.sep + "statistics", mode='wb') as stats_file:
            pickle.dump(session.statistics, stats_file)
        logging.debug('statistics saved')

        # saves the list of protocols
        with open(output_path + os.sep + "list_of_protocols.csv", mode='w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            for i in session.protocols:
                writer.writerow([i])
        logging.debug('list of protocols saved')

        # saves the list of highest protocols
        with open(output_path + os.sep + "list_of_highest_protocols.csv", mode='w', encoding='UTF8',
                  newline='') as file:
            writer = csv.writer(file)
            for i in session.highest_protocols:
                writer.writerow([i])
        logging.debug('list of highest protocols saved')

        # saves runs in a directory
        for x in session.run_results:
            # TODO - REMOVE TEMP FIX?
            run_name = os.sep + "run_" + str(x.timestamp).replace(":", "_").replace(".", "_")
            run_path = output_path + run_name
            logging.info('run from ' + x.timestamp.__str__() + ' saved')
            try:
                os.makedirs(run_path)
            except OSError as err:
                logging.error('Session encoder error: ' + str(err))
                # TODO add error handling
                pass
            # else:
            config_encoder.save(run_path + os.sep + "configuration.csv", x.config)
            with open(run_path + os.sep + "Run_Results", mode='wb') as run_file:
                pickle.dump(x, run_file)
        logging.debug('runs saved')

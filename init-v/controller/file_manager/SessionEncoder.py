import csv
import os
from shutil import copyfile
import pickle

from controller.file_manager.ConfigEncoder import ConfigEncoder

from model.Session import Session
from model.RunResult import RunResult

class SessionEncoder:
    def save(self, output_path: str, session: Session):
        #TODO implement

        try:
            os.makedirs(output_path)
        except OSError:
            #TODO add error handling
            pass

        #copies Pcap in session folder
        copyfile(session.PCAP_PATH, output_path + "\\PCAP.pcapng")

        #saves active configuration in session folder
        config_path = output_path + "\\active_configuration.csv"
        config_encoder = ConfigEncoder()
        config_encoder.save(config_path, session.active_config)

        #saves topology in session folder
        with open(output_path + "\\Topology", mode='wb') as topology:
            pickle.dump(session.topology, topology)

        #saves the list of protocols
        with open(output_path + "\\list_of_protocols.csv", mode = 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            for i in session.protocols:
                writer.writerow([i])


        #saves runs in a directory
        for x in session.run_results:
            run_name = "\\run_" + str(x.timestamp)
            run_path = output_path + run_name
            try:
                os.makedirs(run_path)
            except OSError:
                # TODO add error handling
                pass
            # else:
            config_encoder.save(run_path + "\\configuration.csv", x.config)
            with open(run_path + "\\Run_Results", mode= 'wb') as run_file:
                pickle.dump(x, run_file)

        pass
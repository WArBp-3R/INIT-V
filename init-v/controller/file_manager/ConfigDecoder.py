import csv

from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration

class ConfigDecoder:
    """
    method will decode a Configuration, stored as a .csv file.
    :param source_path: string with the path of the .csv file
    :return Configuration object
    """
    def load_configuration(self, source_path: str) -> Configuration:
        #TODO test
        with open(source_path, mode='r') as file:
            reader = csv.reader(file)
            con = Configuration(None, None, None, None, None, None)
            acon = AutoencoderConfiguration(None, None, None, None, None)
            next(reader)
            for row in reader:

                con.autoencoder = row[0]
                con.pca = row[1]
                con.length_scaling = int(row[2])
                con.normalization = row[3]
                acon.number_of_layers = int(row[4])

                values = row[5].replace("[", "").replace("]", "").split(",")
                result = [int(item) for item in values]

                acon.number_of_nodes = result
                acon.loss_function = row[6]
                acon.number_of_epochs = int(row[7])
                acon.optimizer = row[8]
                con.autoencoder_config = acon
            return con
        pass


import csv

from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration


class ConfigDecoder:

    def load_configuration(self, source_path: str) -> Configuration:
        """
        method will decode a Configuration, stored as a .csv file.
        :param source_path: string with the path of the .csv file
        :return Configuration object
        """
        with open(source_path, mode='r') as file:
            reader = csv.reader(file)
            con = Configuration(None, None, None, None, None, None)
            acon = AutoencoderConfiguration(None, None, None, None, None)
            next(reader)
            for row in reader:

                con.autoencoder = (row[0] == 'True')
                con.pca = (row[1] == 'True')
                con.sample_size = int(row[2])
                con.scaling = row[3]
                con.normalization = row[4]
                acon.number_of_hidden_layers = int(row[5])

                values = row[6].replace("[", "").replace("]", "").split(",")
                result = [int(item) for item in values]

                acon.nodes_of_hidden_layers = result
                acon.loss_function = row[7]
                acon.number_of_epochs = int(row[8])
                acon.optimizer = row[9]
                con.autoencoder_config = acon
            return con

import csv

from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration

#header for the csv file.
header = ['autoencoder', 'pca', 'length_scaling', 'normalization', 'number_of_layers', 'number_of_nodes',
          'loss_function', 'number_of_epochs', 'optimizer']


class ConfigEncoder:
    """
    method to write a Configuration object into a .csv file.

    :param output_path: string of the path to save the .csv at (path || name.csv)
    :param config: Configuration object to be saved

    """
    def save(self, output_path: str, config: Configuration):
        # TODO Test

        data = [config.autoencoder, config.pca, config.length_scaling, config.normalization, config.autoencoder_config.number_of_layers,
                config.autoencoder_config.number_of_nodes, config.autoencoder_config.loss_function, config.autoencoder_config.number_of_epochs, config.autoencoder_config.optimizer]

        with open(output_path, mode = 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(data)

        pass

import csv

from model.Configuration import Configuration


# header for the csv file.
header = ['autoencoder', 'pca', 'sample_size', 'scaling', 'normalization', 'number_of_hidden_layers',
          'nodes_of_hidden_layers',
          'loss_function', 'number_of_epochs', 'optimizer']


class ConfigEncoder:

    def save(self, output_path: str, config: Configuration):
        """
        method to write a Configuration object into a .csv file.
        :param output_path: string of the path to save the .csv at (path || name.csv)
        :param config: Configuration object to be saved

        """
        # TODO Test

        data = [config.autoencoder, config.pca, config.sample_size, config.scaling, config.normalization,
                config.autoencoder_config.number_of_hidden_layers,
                config.autoencoder_config.nodes_of_hidden_layers, config.autoencoder_config.loss_function,
                config.autoencoder_config.number_of_epochs, config.autoencoder_config.optimizer]

        with open(output_path, mode='w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(data)

        pass

from model.Configuration import Configuration


def configuration_equal(c1: Configuration, c2: Configuration) -> bool:
    a1 = c1.autoencoder_config
    a2 = c2.autoencoder_config
    p1 = (c1.pca == c2.pca) and (c1.normalization == c2.normalization) and (c1.length_scaling == c2.length_scaling)
    p2 = (c1.autoencoder == c2.autoencoder) and (a1.optimizer == a2.optimizer)
    p3 = (a1.number_of_nodes == a2.number_of_nodes) and (a1.number_of_layers == a2.number_of_layers)
    p4 = (a1.number_of_epochs == a2.number_of_epochs) and (a1.loss_function == a2.loss_function)

    return p1 and p2 and p3 and p4

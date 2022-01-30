import random
import string

from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration

"""creates a randomized configuration"""


def create_rand_config() -> Configuration:
    nol = bool(random.getrandbits(1))
    non = [random.randint(1, 1000) for i in range(random.randint(0, 100))]
    lf = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(0, 20)))
    noe = random.randint(0, 100)
    # maybe begin with 1?
    opt = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(0, 20)))

    a = AutoencoderConfiguration(nol, non, lF, noe, opt)

    autoencoder = bool(random.getrandbits(1))
    pca = bool(random.getrandbits(1))
    ls = random.randint(-100, 100)
    norm = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(0, 20)))

    c = Configuration(autoencoder, pca, ls, norm, a)

    return c

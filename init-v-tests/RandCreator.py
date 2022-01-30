import random
import string

from keras.callbacks import History

from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from model.MethodResult import MethodResult
from model.PerformanceResult import PerformanceResult
from model.Statistics import Statistics
from model.Session import Session

"""creates a randomized configuration"""

s1 = -100
s2 = 0
s3 = 1
e1 = 100
e2 = 10**4
e3 = 10**6

def create_rand_method_result() -> MethodResult:
    pca_r = [(random.uniform(s1, e1), random.uniform(s1, e1), (''.join(random.choice(string.ascii_letters) for _ in
            range(random.randint(0, 20))))) for _2 in range(random.randint(s3, e3))]
    aut_r = [(random.uniform(s1, e1), random.uniform(s1, e1), (''.join(random.choice(string.ascii_letters) for _ in
            range(random.randint(0, 20))))) for _2 in range(random.randint(s3, e3))]
    return MethodResult(pca_r, aut_r)

def create_rand_performance_result() -> PerformanceResult:
    # TODO create rand History
    hist: History = None
    pca: [(random.uniform(s1, e1), random.uniform(s1, e1)) for _ in range(random.randint(s3, e3))]
    return PerformanceResult(pca, hist)




def create_rand_config() -> Configuration:
    nol = bool(random.getrandbits(1))
    non = [random.randint(1, 1000) for i in range(random.randint(0, 100))]
    lf = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(0, 20)))
    noe = random.randint(0, 100)
    # maybe begin with 1?
    opt = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(0, 20)))

    a = AutoencoderConfiguration(nol, non, lf, noe, opt)

    autoencoder = bool(random.getrandbits(1))
    pca = bool(random.getrandbits(1))
    ls = random.randint(-100, 100)
    norm = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(0, 20)))

    c = Configuration(autoencoder, pca, ls, norm, a)

    return c

def create_rand_session() -> Session:

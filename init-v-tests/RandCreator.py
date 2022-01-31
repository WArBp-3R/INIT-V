import random
import string
import datetime

import keras.callbacks
from keras.callbacks import History

from model.network.NetworkTopology import NetworkTopology
from model.network.Device import Device
from model.network.Connection import Connection
from model.IStatistic import IStatistic
from model.Configuration import Configuration
from model.AutoencoderConfiguration import AutoencoderConfiguration
from model.MethodResult import MethodResult
from model.PerformanceResult import PerformanceResult
from model.Statistics import Statistics
from model.RunResult import RunResult
from model.Session import Session

"""creates a randomized configuration"""

# TODO: match up number of packets and points in results with topology and maybe strs too?

s1 = -100
s2 = 0
s3 = 1
m1 = 20
e1 = 100
e2 = 10 ** 4
e3 = 10 ** 6

"""creates a randomized method result with n packets if n>=0 otherwise with a random number between s3 and e3 packets"""


def create_rand_method_result(n: int) -> MethodResult:
    r = range(random.randint(s3, e3))
    if n >= 0:
        r = range(n)

    pca_r = [(random.uniform(s1, e1), random.uniform(s1, e1), (''.join(random.choice(string.ascii_letters) for _ in
                                                                       range(random.randint(0, 20))))) for _2 in r]
    aut_r = [(random.uniform(s1, e1), random.uniform(s1, e1), (''.join(random.choice(string.ascii_letters) for _ in
                                                                       range(random.randint(0, 20))))) for _2 in r]
    return MethodResult(pca_r, aut_r)


"""creates a randomized performance result"""


def create_rand_performance_result() -> PerformanceResult:
    # TODO create rand History
    hist: History = keras.callbacks.History()
    pca = [(random.uniform(s1, e1), random.uniform(s1, e1)) for _ in range(random.randint(s3, e3))]
    return PerformanceResult(pca, hist)


"""creates a randomized statistics object"""


def create_rand_statistics() -> Statistics:
    # TODO: get some stats
    statlist: list[IStatistic] = []
    return Statistics(statlist)


"""creates a randomized configuration"""


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


"""creates randomized run result with n packets if n>=0 otherwise a randomized number of packets"""


def create_rand_run_result(n: int) -> RunResult:
    # TODO: maybe add randomized time
    t = datetime.now()
    mr = create_rand_method_result(n)
    pr = create_rand_performance_result()
    cfg = create_rand_config()
    stats = create_rand_statistics()
    return RunResult(t, cfg, mr, stats, pr)


def create_rand_network_topology(n_c: int, n_d: int) -> NetworkTopology:
    # TODO: implement
    pass


"""creates a randomized set of n or a random number between 1 and 20 strings if n == 0"""


def create_rand_protocols(n: int) -> set[str]:
    r = range(random.randint(s3, m1))
    if n >= 0:
        r = range(n)

    return set([(''.join(random.choice(string.ascii_letters) for _ in range(random.randint(0, 20)))) for _ in r])


"""creates a session object with n_pa packets, n_p protocols, n_d devices and n_c connections. If any of those is equal 
to zero or less, it is replaced by a randomized value. In addition the max_density variable is used to set the maximum
factor of possible connections"""


def create_rand_session(n_pa: int, n_p: int, n_d: int, n_c: int, max_density: float) -> Session:
    density_factor = 10**(-3)
    if 1 >= max_density >= 0:
        density_factor = max_density
    pa = random.randint(s3, e3)
    p = random.randint(s3, m1)
    d = random.randint(s3, e1)
    c = random.randint(s3, density_factor * (d-1) * d / 2)
    if n_pa >= 1:
        pa = n_pa
    if n_p >= 1:
        p = n_p
    if n_d >= 1:
        d = n_d
    if n_c >= 1:
        c = n_c
    path = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(0, 20)))
    protocols = create_rand_protocols(p)
    topology = create_rand_network_topology(c, d)
    run_r = [create_rand_run_result(pa) for _ in range(s3, m1)]
    a_c = create_rand_config()
    return Session(path, protocols, run_r, a_c, topology, None)

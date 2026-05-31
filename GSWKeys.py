import numpy as np

from GSWParams import *
from GSWGadgets import *


class SecretKey:

    def __init__(self, params: GSWParams):
        n = params.get_n()
        q = params.get_q()
        ell = params.get_ell()
        t = np.random.randint(0, q, size=(n,1)) # Samples t in Z_q^n
        s = np.concatenate((np.array([[1]]), -t), axis=0) % q # s = (1,-t) so A*s=e
        v = PowersOf2(s, ell, q) # Approximate eigenvector
        self.__t = t
        self.__s = s
        self.__v = v

    def getSecretKey(self) -> np.ndarray:
        return self.__s

    def get_t(self) -> np.ndarray:
        return self.__t

    def get_v(self) -> np.ndarray:
        return self.__v


class PublicKey:

    def __init__(self, sk: SecretKey, params: GSWParams):
        n = params.get_n()
        q = params.get_q()
        m = params.get_m()
        sigma = params.get_sigma()

        B = np.random.randint(0, q, size=(m,n))
        e = np.round(np.random.normal(0, sigma, size=(m,1))).astype(np.int64) # Error around 0
        b = (B @ sk.get_t() + e) % q
        self.A = np.concatenate((b, B), axis=1)

    def getPublicKey(self) -> np.ndarray:
        return self.A

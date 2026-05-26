import numpy as np

from GSWParams import *
from GSWGadgets import *


class SecretKey:

    def __init__(self, params: GSWParams):
        n = params.get_n()
        q = params.get_q()
        ell = params.get_ell()
        t = np.random.randint(0, q, size=(n,1))
        s = np.concatenate((np.array([[1]]), -t), axis=0)
        v = PowersOf2(s, ell, q)
        self.__t = t
        self.__s = s
        self.__v = v

    def getSecretKey(self) -> np.ndarray:
        return self.__s

    def generatePublicKey(self, params: GSWParams) -> np.ndarray:
        n = params.get_n()
        q = params.get_q()
        m = params.get_m()
        sigma = params.get_sigma()

        B = np.random.randint(0, q, size=(m,n))
        e = np.round(np.random.normal(0, sigma, size=(m,1))).astype(np.int64) % q
        b = (B @ self.__t + e) % q
        A = np.concatenate((b, B), axis=1)
        return A


class PublicKey:

    def __init__(self, sk: SecretKey, params: GSWParams):
        self.A = sk.generatePublicKey(params)

    def getPublicKey(self) -> np.ndarray:
        return self.A

# TODO Testes:
params = GSWParams(n=3, q=16, sigma=3.2)
g = SecretKey(params)
print(g.getSecretKey())
pk = PublicKey(g, params)
print(pk.getPublicKey())

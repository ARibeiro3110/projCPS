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
    
    def gett(self) -> np.ndarray:
        return self.__t

class PublicKey:

    def __init__(self, sk: SecretKey, params: GSWParams):
        n = params.get_n()
        q = params.get_q()
        m = params.get_m()
        sigma = params.get_sigma()

        B = np.random.randint(0, q, size=(m,n))
        e = np.round(np.random.normal(0, sigma, size=(m,1))).astype(np.int64) #Não é mod q pq o erro tem q ser à volta de 0
        print("error e:\n", e)
        b = (B @ sk.gett() + e) % q
        self.A = np.concatenate((b, B), axis=1)


    def getPublicKey(self) -> np.ndarray:
        return self.A


if __name__ == "__main__": # TODO Testes:
    params = GSWParams(L=5, n=3, q=16)
    g = SecretKey(params)
    print(g.gett())
    print(g.getSecretKey())
    pk = PublicKey(g, params)
    print(pk.getPublicKey())

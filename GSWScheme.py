from GSWParams import *
import numpy as np
from GSWGadgets import *
from GSWKeys import *

class GSW:
    def __init__(self, seed: int | None = None):
        self.params = None
        self.__sk = None
        self.pk = None
        self.rng = np.random.default_rng(seed)

    def Setup(self, L: int, n: int, q: int) -> None: #chi: callable, m: int
        self.params = GSWParams(L=L,n=n, q=q)

    def SecretKeyGen(self) -> SecretKey:
        sk= SecretKey(self.params)
        self.__sk = sk

    def PublicKeyGen(self) -> PublicKey:
        pk= PublicKey(self.__sk, self.params)
        self.pk=pk

    def Enc(self, mu: int) -> np.ndarray:
        R=np.random.randint(0,2,size=(self.params.getN(), self.params.getm()))
        C=FlattenMatrix(mu * np.eye(self.params.getN(), dtype=np.int64) + BitDecompMatrix(R@self.pk.getPublicKey(), self.params.getell(), self.params.getq()), self.params.getell(), self.params.getq())
        return C

    def Dec(self, sk: SecretKey, C: np.ndarray) -> int:
        pass

    def MPDec(self, sk: SecretKey, C: np.ndarray) -> int:
        pass

    def MultConst(self, C: np.ndarray, alpha: int) -> np.ndarray:
        M_alpha = FlattenMatrix(
            alpha * np.eye(self.params.getN(), dtype=np.int64) % self.params.q,
            self.params.getell(),
            self.params.getq()
        )
        return FlattenMatrix(
            (M_alpha @ C) % self.params.getq(),
            self.params.getell(),
            self.params.getq()
        )

    def Add(self, C1: np.ndarray, C2: np.ndarray) -> np.ndarray:
        return FlattenMatrix(
            (C1 + C2) % self.params.getq(),
            self.params.getell(),
            self.params.getq()
        )

    def Mult(self, C1: np.ndarray, C2: np.ndarray) -> np.ndarray:
        return FlattenMatrix(
            (C1 @ C2) % self.params.getq(),
            self.params.getell(),
            self.params.getq()
        )

    def NAND(self, C1: np.ndarray, C2: np.ndarray) -> np.ndarray:
        return FlattenMatrix(
            (np.eye(self.params.N, dtype=np.int64) - (C1 @ C2)) % self.params.q,
            self.params.ell,
            self.params.q
        )

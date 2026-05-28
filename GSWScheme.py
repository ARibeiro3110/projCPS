import numpy as np

from GSWParams import *
from GSWGadgets import *
from GSWKeys import *


class GSWScheme:

    def __init__(self, seed: int | None = None):
        self.params = None
        self.__sk = None
        self.pk = None
        self.rng = np.random.default_rng(seed) # TODO: isto não está a ser usado

    def Setup(self, L: int, n: int, q: int) -> None:
        self.params = GSWParams(L=L, n=n, q=q)

    def SecretKeyGen(self) -> SecretKey:
        self.__sk = SecretKey(self.params)
        return self.__sk.getSecretKey()

    def PublicKeyGen(self) -> PublicKey:
        self.pk = PublicKey(self.__sk, self.params)
        return self.pk

    def getPublicKey(self) -> PublicKey:
        return self.pk

    def Enc(self, pk: PublicKey, mu: int) -> np.ndarray:
        q = self.params.get_q()
        ell = self.params.get_ell()
        N = self.params.get_N()
        m = self.params.get_m()

        R = np.random.randint(0, 2, size=(N, m))
        C = FlattenMatrix(
            mu * np.eye(N, dtype=np.int64) + BitDecompMatrix(R @ pk.A, ell, q),
            ell,
            q
        )
        return C

    def Dec(self, sk: SecretKey, C: np.ndarray) -> int:
        pass

    def MPDec(self, sk: SecretKey, C: np.ndarray) -> int:
        pass

    def MultConst(self, C: np.ndarray, alpha: int) -> np.ndarray:
        ell = self.params.get_ell()
        q = self.params.get_q()
        N = self.params.get_N()

        M_alpha = FlattenMatrix(
            alpha * np.eye(N, dtype=np.int64) % q,
            ell,
            q
        )
        return FlattenMatrix(
            (M_alpha @ C) % q,
            ell,
            q
        )

    def Add(self, C1: np.ndarray, C2: np.ndarray) -> np.ndarray:
        ell = self.params.get_ell()
        q = self.params.get_q()

        return FlattenMatrix(
            (C1 + C2) % q,
            ell,
            q
        )

    def Mult(self, C1: np.ndarray, C2: np.ndarray) -> np.ndarray:
        ell = self.params.get_ell()
        q = self.params.get_q()

        return FlattenMatrix(
            (C1 @ C2) % q,
            ell,
            q
        )

    def NAND(self, C1: np.ndarray, C2: np.ndarray) -> np.ndarray:
        ell = self.params.get_ell()
        q = self.params.get_q()

        return FlattenMatrix(
            (np.eye(self.params.get_N(), dtype=np.int64) - (C1 @ C2)) % q,
            ell,
            q
        )

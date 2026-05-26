from GSWParams import *
import numpy as np
from GSWGadgets import *

class GSW:
    def __init__(self, seed: int | None = None):
        self.params = None
        self.rng = np.random.default_rng(seed)

    def Setup(self, L: int, n: int, q: int) -> None: #chi: callable, m: int
        self.params = GSWParams(L=L,n=n, q=q)

    def SecretKeyGen(self) -> SecretKey:
        pass

    def PublicKeyGen(self, sk: SecretKey) -> PublicKey:
        pass

    def Enc(self, pk: PublicKey, mu: int) -> np.ndarray:
        pass

    def Dec(self, sk: SecretKey, C: np.ndarray) -> int:
        pass

    def MPDec(self, sk: SecretKey, C: np.ndarray) -> int:
        pass

    def MultConst(self, C: np.ndarray, alpha: int) -> np.ndarray:
        M_alpha = FlattenMatrix(
            alpha * np.eye(self.params.N, dtype=np.int64) % self.params.q,
            self.params.ell,
            self.params.q
        )
        return FlattenMatrix(
            (M_alpha @ C) % self.params.q,
            self.params.ell,
            self.params.q
        )

    def Add(self, C1: np.ndarray, C2: np.ndarray) -> np.ndarray:
        return FlattenMatrix(
            (C1 + C2) % self.params.q,
            self.params.ell,
            self.params.q
        )

    def Mult(self, C1: np.ndarray, C2: np.ndarray) -> np.ndarray:
        return FlattenMatrix(
            (C1 @ C2) % self.params.q,
            self.params.ell,
            self.params.q
        )

    def NAND(self, C1: np.ndarray, C2: np.ndarray) -> np.ndarray:
        return FlattenMatrix(
            (np.eye(self.params.N, dtype=np.int64) - (C1 @ C2)) % self.params.q,
            self.params.ell,
            self.params.q
        )

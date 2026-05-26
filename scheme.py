from dataclasses import dataclass
import numpy as np

from gadgets import *


@dataclass(frozen=True)
class GSWParams:
    n: int
    q: int
    chi: callable
    m: int
    ell: int
    N: int


@dataclass(frozen=True)
class SecretKey:
    s: np.ndarray
    v: np.ndarray


@dataclass(frozen=True)
class PublicKey:
    A: np.ndarray


class GSWScheme:
    def __init__(self, seed: int | None = None):
        self.params = None
        self.rng = np.random.default_rng(seed)

    def Setup(self, n: int, q: int, chi: callable, m: int) -> None:
        ell = int(np.ceil(np.log2(q))) + 1
        N = (n + 1) * ell
        self.params = GSWParams(n=n, q=q, chi=chi, m=m, ell=ell, N=N)

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

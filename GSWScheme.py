import numpy as np

from GSWParams import *
from GSWGadgets import *
from GSWKeys import *


class GSWScheme:

    def __init__(self):
        self.params = None
        self.pk = None

    def Setup(self, L: int, n: int, q: int, hardness: str = "standard") -> None:
        self.params = GSWParams(L=L, n=n, q=q, hardness=hardness)

    def SecretKeyGen(self) -> SecretKey:
        return SecretKey(self.params)

    def PublicKeyGen(self, sk: SecretKey) -> PublicKey:
        self.pk = PublicKey(sk, self.params)

    def getPublicKey(self) -> PublicKey:
        return self.pk

    def Enc(self, pk: PublicKey, mu: int) -> np.ndarray:
        q = self.params.get_q()
        ell = self.params.get_ell()
        N = self.params.get_N()
        m = self.params.get_m()

        R = np.random.randint(0, 2, size=(N, m)) # Uniform matrix in {0,1}^{N*m}
        C = FlattenMatrix( # C=Flatten(mu*I_N + BitDecomp(R*A))
            mu * np.eye(N, dtype=np.int64) + BitDecompMatrix(R @ pk.getPublicKey(), ell, q),
            ell,
            q
        )
        return C

    def Dec(self, sk: SecretKey, C: np.ndarray) -> int:
        q = self.params.get_q()
        i = int(np.floor(np.log2(q))) - 1 # v_i in ]q/4, q/2]
        v = sk.get_v()
        x = (C[i] @ v) % q
        x_centered = ((x + q // 2) % q) - q // 2 # Center around 0
        return round(x_centered/v[i]) % 2

    def CalculateDecError(self, sk: SecretKey, C: np.ndarray, mu: int) -> int:
        q = self.params.get_q()
        i = int(np.floor(np.log2(q)))-1
        v = sk.get_v()
        e = C[i] @ v - mu * v[i]
        e_centered = ((e + q // 2) % q) - q // 2
        return abs(e_centered)

    def MPDec(self, sk: SecretKey, C: np.ndarray) -> int:
        q = self.params.get_q()
        l = self.params.get_ell()
        v = sk.get_v()
        mu = 0

        for i in range(l-1):
            shift = (l - 2) - i
            val = ((C[shift] @ v) % q) - (mu << shift) # Equivalent to mu*(2**shift)
            val_centered = ((val + q // 2) % q) - q // 2
            if abs(val_centered) > q // 4: # If the value is closer to q/2 than to 0, decode a 1
                mu |= (1 << i) # Equivalent to += (2 ** i)
        return mu


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

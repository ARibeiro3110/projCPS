import numpy as np

from GSWParams import *
from GSWGadgets import *
from GSWKeys import *


class GSWScheme:

    def __init__(self, seed: int | None = None):
        self.params = None
        #self.__sk = None
        self.pk = None
        self.rng = np.random.default_rng(seed) # TODO: isto não está a ser usado

    def Setup(self, L: int, n: int, q: int) -> None:
        self.params = GSWParams(L=L, n=n, q=q)

    def SecretKeyGen(self) -> SecretKey:
        return SecretKey(self.params)

    def PublicKeyGen(self, sk: SecretKey) -> PublicKey:
        self.pk = PublicKey(sk, self.params)
        #return self.pk

    def getPublicKey(self) -> PublicKey:
        return self.pk

    def Enc(self, pk: PublicKey, mu: int) -> np.ndarray:
        q = self.params.get_q()
        ell = self.params.get_ell()
        N = self.params.get_N()
        m = self.params.get_m()

        R = np.random.randint(0, 2, size=(N, m))
        C = FlattenMatrix(
            mu * np.eye(N, dtype=np.int64) + BitDecompMatrix(R @ pk.getPublicKey(), ell, q),
            ell,
            q
        )
        return C

    def Dec(self, sk: SecretKey, C: np.ndarray) -> int:
        q=self.params.get_q()
        i=int(np.floor(np.log2(q)))-1
        v = PowersOf2(sk.getSecretKey(), self.params.get_ell(), q)
        x=(C[i] @ v) % q
        print("v:\n", v[i])
        x_centered=((x + q // 2) % q) - q // 2 #Como mensagens pequenas centramos em 0
        print("x:", x)
        #print("x_centered:", x_centered)
        return round(x_centered/v[i])%2  #TODO: Confirmar se há maneira de fazer sem usar mod 2

    def MPDec(self, sk: SecretKey, C: np.ndarray) -> int:
        q=self.params.get_q()
        l=self.params.get_ell()
        v=PowersOf2(sk.getSecretKey(), self.params.get_ell(), q)
        mu=0
        for i in range(l-1):
            val= ((C[l-2-i] @ v)%q) - mu*(2**(l-2-i))
            
            val_centered = ((val + q // 2) % q) - q // 2

            if abs(val_centered) > q // 4:
                mu += (2 ** i)
        return mu #TODO: Testar

        

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


scheme = GSWScheme(seed=1)
scheme.Setup(L=1, n=3, q=1536)
print("Parameters:\n ", scheme.params)
sk = scheme.SecretKeyGen()
scheme.PublicKeyGen(sk)
pk=scheme.getPublicKey()
print("Parameters:\n ", scheme.params)
print("Secret Key:\n", sk.getSecretKey())
print("Public Key:\n", pk.getPublicKey())
print("error e:\n", pk.getPublicKey()@sk.getSecretKey()%scheme.params.get_q())
C1 = scheme.Enc(pk, mu=0)
C2 = scheme.Enc(pk, mu=1)
C3 = scheme.NAND(C1, C2)
print("Decrypted 1:\n", scheme.Dec(sk, C1))
print("Decrypted 2:\n", scheme.Dec(sk, C2))
print("NAND Result:\n", scheme.Dec(sk, C3))
C4 = scheme.Enc(pk, mu=14)
print("Decrypted 4:\n", scheme.MPDec(sk, C4))
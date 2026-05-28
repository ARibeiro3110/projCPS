from numpy import ceil, log2

class GSWParams:

    def __init__(self, L:int, n: int, q: int, k: int = 5):
        self.L = L
        self.n = n
        self.q = q
        self.ell = int(ceil(log2(q))) + 1
        self.N = self.ell * (self.n + 1)
        self.m = self.ell * self.n
        self.sigma = 1.0 #q/(k*(8*(self.N+1)**self.L)) # TODO: Confirmar valor de k e add toy parameters and real parameters

    def get_n(self) -> int:
        return self.n

    def get_q(self) -> int:
        return self.q

    def get_sigma(self) -> float:
        return self.sigma

    def get_ell(self) -> int:
        return self.ell

    def get_N(self) -> int:
        return self.N

    def get_m(self) -> int:
        return self.m

    def __str__(self) -> str:
        return f"GSWParams(n={self.n}, q={self.q}, sigma={self.sigma}, ell={self.ell}, N={self.N}, m={self.m})"

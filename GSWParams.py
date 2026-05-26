from numpy import ceil, log2

class GSWParams:
    
    def __init__(self, L, n, q):
        self.L = L
        self.n = n
        self.q = q
        self.sigma = 3.2 #Mudar depois para ser tal que prob B negligible
        self.l= int(ceil(log2(q))) + 1
        self.m = self.l*self.n
        self.N = self.l*(self.n+1)
    
    def getn(self):
        return self.n
    
    def getq(self):
        return self.q
    
    def getell(self):
        return self.l
    
    def getm(self):
        return self.m
    
    def getN(self):
        return self.N
    
    def getSigma(self):
        return self.sigma

    def __str__(self):
        return f"GSWParams(L={self.L}, n={self.n}, q={self.q}, sigma={self.sigma}, l={self.l}, m={self.m}, N={self.N})"

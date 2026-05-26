import numpy as np
from gadgets import *
from GSWParams import GSWParams

class SecretKey:

    def __init__(self, params):#Substituir depois por params
        n = params.getn()
        q = params.getq()
        l = params.getell()
        t= np.random.randint(0,q,size=(n,1))
        sk=[1]+ -t
        v= PowersOf2(sk,l,q)
        self.__t=t
        self.__sk=sk
        self.__v=v
    
    def PublicKey(self,params):
        n = params.getn()
        q = params.getq()
        m = params.getm()
        sigma = params.getSigma()

        B=np.random.randint(0,q,size=(m,n))
        e=np.round(np.random.normal(0,sigma,size=(m,1))).astype(int)%q
        b=(B @self.__t+ e)%q
        A = np.concatenate((b,B), axis=1)
        return A

    def getSecretKey(self): #Adicionar password depois
        return self.__sk



class PublicKey:
    def __init__(self, sk: SecretKey, params: GSWParams):
        self.pk=sk.PublicKey(params)

    def getPublicKey(self):
        return self.pk


params = GSWParams(L=2, n=3, q=16)
g= SecretKey(params)
print(g.getSecretKey())
pk= PublicKey(g, params)
print(pk.getPublicKey())
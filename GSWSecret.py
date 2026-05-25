import numpy as np
from utils import *
class GSWKey:

    def __init__(self, n, q,l,m):#Substituir depois por params
        t= np.random.randint(0,q,size=(n,1))
        sk=[1]+ -np.array(t)
        v= Powerof2(sk,l)
        self.__t=t
        self.__sk=sk
        self.__v=v
    
    def PublicKey(self,n,q,l,m, sigma):
        B=np.random.randint(0,q,size=(m,n))
        e=np.round(np.random.normal(0,sigma,size=(m,1))).astype(int)%q
        b=(B @self.__t+ e)%q
        A = np.concatenate((b,B), axis=1)
        return A

    def getSecretKey(self): #Adicionar password depois
        return self.__sk


g= GSWKey(4,16,4,3)
print(np.random.randint(0,16,size=(3,4)))
print(g.PublicKey(4,16,4,3,0.1))
from GSWParams import *
from GSWGadgets import *
from GSWKeys import *
from GSWScheme import *


import numpy as np

scheme = GSWScheme()
q=2**15
n=8
scheme.Setup(L=0, n=n, q=q, hardness="toy")
ell = scheme.params.get_ell()
max_mu = q - 1
print("\nTesting Homomorphic Operations for \n", scheme.params, "\n")

sk = scheme.SecretKeyGen()

scheme.PublicKeyGen(sk)

pk = scheme.getPublicKey()

mu1 = np.random.randint(0, q)
mu2 = np.random.randint(0, q)

C1 = scheme.Enc(pk, mu=mu1)
print("mu1:", mu1)
print("Decrypted 1:", scheme.MPDec(sk, C1))

C2 = scheme.Enc(pk, mu=mu2)
print("\nmu2:", mu2)
print("Decrypted 2:", scheme.MPDec(sk, C2))


print("\n##### ADD #####")

Cadd = scheme.Add(C1, C2)
muadd = (mu1 + mu2) % scheme.params.get_q()
print("mu:", muadd)
print("Decrypted Add:", scheme.MPDec(sk, Cadd))

print("\n##### CONST MULT #####")
alpha = 2
Cconst = scheme.MultConst(C1, alpha)
muconst = (alpha * mu1) % scheme.params.get_q()
print("mu:", muconst)
print("Decrypted ConstMult:", scheme.MPDec(sk, Cconst))

print("\n##### MULT #####\n")
print("\n##### MULT #####")
Cmult = scheme.Mult(C1, C2)
mumult = (mu1 * mu2) % scheme.params.get_q()
print("mu:", mumult)
print("Decrypted Mult:", scheme.MPDec(sk, Cmult))

mu3=0
C3 = scheme.Enc(pk, mu=mu3)
mu4=1
C4 = scheme.Enc(pk, mu=mu4)
Cmult3 = scheme.Mult(C1, C3)
mumult3 = (mu1 * mu3) % scheme.params.get_q()
print("\nmumult3:", mumult3)
print("Decrypted Mult:", scheme.MPDec(sk, Cmult3))

Cmult4 = scheme.Mult(C1, C4)
mumult4 = (mu1 * mu4) % scheme.params.get_q()
print("\nmumult4:", mumult4)
print("Decrypted Mult:", scheme.MPDec(sk, Cmult4))

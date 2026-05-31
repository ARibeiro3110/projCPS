from GSWParams import *
from GSWGadgets import *
from GSWKeys import *
from GSWScheme import *



scheme = GSWScheme()
scheme.Setup(L=0, n=8, q=2**15, hardness="standard")
print("Testing GSW Scheme for parameters\n", scheme.params)

sk = scheme.SecretKeyGen()
scheme.PublicKeyGen(sk)
pk=scheme.getPublicKey()
print("Secret Key:\n", sk.getSecretKey())
#print("Public Key:\n", pk.getPublicKey())
#print("error e:\n", pk.getPublicKey()@sk.getSecretKey()%scheme.params.get_q())

mu1 = 0
mu2 = 1
C1 = scheme.Enc(pk, mu=mu1)
print("Decrypted 1:\n", scheme.Dec(sk, C1))
print("Abs error 1:\n", scheme.DecTest(sk, C1, mu=0))
C2 = scheme.Enc(pk, mu=mu2)
print("Decrypted 2:\n", scheme.Dec(sk, C2))
print("Abs error 2:\n", scheme.DecTest(sk, C2, mu=mu2))
#C3 = scheme.NAND(C1, C2)
for i in range(5):
    print("Iteration:\n", i+1)
    C = scheme.NAND(C1, C2)
    mu = (0 if mu1 == 1 and mu2 == 1 else 1)
    print("mu:", mu)
    print("Decrypted NAND:\n", scheme.Dec(sk, C))
    e=scheme.DecTest(sk, C, mu=mu)
    print("Abs error NAND:\n", e)
    print(e<scheme.params.get_q()/8)
    C1=C2
    mu1=mu2
    C2=C
    mu2=mu


#print("NAND Result:\n", scheme.Dec(sk, C3))
C4 = scheme.Enc(pk, mu=14)
print("Decrypted 4:\n", scheme.MPDec(sk, C4))
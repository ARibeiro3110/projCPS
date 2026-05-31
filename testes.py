from GSWParams import *
from GSWGadgets import *
from GSWKeys import *
from GSWScheme import *



scheme = GSWScheme()
scheme.Setup(L=3, n=4, q=2**30, hardness="standard")
print("\nTesting GSW Scheme for parameters\n", scheme.params, "\n")

sk = scheme.SecretKeyGen()
scheme.PublicKeyGen(sk)
pk=scheme.getPublicKey()
#print("Secret Key:\n", sk.getSecretKey())
#print("Public Key:\n", pk.getPublicKey())
#print("error e:\n", pk.getPublicKey()@sk.getSecretKey()%scheme.params.get_q())

mu1 = 0
mu2 = 1
C1 = scheme.Enc(pk, mu=mu1)
print("mu1:", mu1)
print("Decrypted 1:", scheme.Dec(sk, C1))
print("Error Decryption 1:", scheme.DecTest(sk, C1, mu=mu1))
C2 = scheme.Enc(pk, mu=mu2)
print("\nmu2:", mu2)
print("Decrypted 2:", scheme.Dec(sk, C2))
print("Error Decryption 2:", scheme.DecTest(sk, C2, mu=mu2))

for i in range(5):

    print("\n##### Iteration:", f"{i+1}", "#####")
    C = scheme.NAND(C1, C2)
    mu = (0 if mu1 == 1 and mu2 == 1 else 1)
    print("mu:", mu)
    print("Decrypted NAND:", scheme.Dec(sk, C))
    e=scheme.DecTest(sk, C, mu=mu)
    print("Error Decryption NAND:", e)
    print("Error < q/8:", e<scheme.params.get_q()/8)
    C1=C2
    mu1=mu2
    C2=C
    mu2=mu





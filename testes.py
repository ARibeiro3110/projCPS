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



 
import numpy as np
 
NUM_SAMPLES = 5  # número de mu aleatórios por configuração (excluindo mu=0)
 
# Pares (n, q): q escolhido como potência de 2 adequada a cada n
CONFIGS = [
    (4,  2**14),
    (8,  2**20),
    (16, 2**30),
]
 
for (n, q) in CONFIGS:
 
    scheme = GSWScheme()
    scheme.Setup(L=0, n=n, q=q, hardness="toy")
    ell = scheme.params.get_ell()
    max_mu = 2 ** (ell - 1) - 1  # range válido para MPDec
 
    print("=" * 60)
    print(f"Parâmetros: n={n}, q={q}")
    print(f"  {scheme.params}")
    print(f"  Range válido de mu: [0, {max_mu}] ({ell-1} bits)\n")
 
    sk = scheme.SecretKeyGen()
    scheme.PublicKeyGen(sk)
    pk = scheme.getPublicKey()
 
    # mu=0 incluído sempre; depois NUM_SAMPLES aleatórios em Z_q
    mus = [0] + [int(np.random.randint(0, q)) for _ in range(NUM_SAMPLES)]
 
    failures = 0
    for mu in mus:
        C = scheme.Enc(pk, mu=mu)
        mu_dec = scheme.MPDec(sk, C)
        correct = (mu_dec == mu)
        if not correct:
            failures += 1
 
        in_range = (mu <= max_mu)
        tag = "" if in_range else "  [mu fora do range válido de MPDec]"
        status = "OK" if correct else "FALHOU"
        print(f"  mu={mu:<12}  MPDec={mu_dec:<12}  [{status}]{tag}")
 
    print(f"\n  Taxa de falha: {failures}/{len(mus)}")
    print()

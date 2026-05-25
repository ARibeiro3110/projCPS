from numpy import ceil, log2

def BitDecomp(a, l): # dima=k
    r=[]
    for x in a:
        for j in range(l):
            r.append((x>>j) & 1) #Bitwise Shift and & 1 to get the j-th bit of x, faster than using % and //.
    return r #dimr=N

def BitDecompMatrix(a,l): 
    r=[]
    for i in range(len(a)):
        r.append(BitDecomp(a[i],l))
    return r

def BitDecompInv(a,l):# dima=N=k*l
    r=[]
    for x in range(0, len(a), l):
        v=0
        for j in range(l):
            v+=2**j * a[x+j]
        r.append(v)
    return r #dimr=k

def BitDecompInvMatrix(a,l):
    r=[]
    for i in range(len(a)):
        r.append(BitDecompInv(a[i],l))
    return r

def Flatten(a,l):# dima=N
    return BitDecomp(BitDecompInv(a,l),l) #dim=N

def FlattenMatrix(a,l):
    return BitDecompMatrix(BitDecompInvMatrix(a,l),l)

def Powerof2(b,l):#dimb=k
    r=[]
    for x in b:
        for j in range(l):
            r.append(2**j*x)
    return r #dimr=N



print(BitDecomp([6,3],4))
print(6>>1)
print(BitDecompInv(BitDecomp([6,3],4),4))
print(Flatten([6,3,4,5,1,0,2,1],4))

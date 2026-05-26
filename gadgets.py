import numpy as np

def PowersOf2(b: np.ndarray, ell: int, q: int) -> np.ndarray: # dim(b) = k
    r = []
    for x in b:
        for j in range(ell):
            r.append((1 << j) * int(x) % q)
    return np.array(r, dtype=np.int64) # dim = N = k * ell

def BitDecompVector(a: np.ndarray, ell: int, q: int) -> np.ndarray: # dim(a) = k
    r = []
    for x in a:
        x = int(x) % q
        for j in range(ell):
            r.append((x >> j) & 1)
    return np.array(r, dtype=np.int64) # dim = N = k * ell

def BitDecompMatrix(A: np.ndarray, ell: int, q: int) -> np.ndarray:
    return np.array([BitDecompVector(row, ell, q) for row in A], dtype=np.int64)

def BitDecompInvVector(a: np.ndarray, ell: int, q: int) -> np.ndarray: # dim(a) = N = k * ell
    r = []
    for x in range(0, len(a), ell):
        v = 0
        for j in range(ell):
            v += int(a[x + j]) << j
        r.append(v % q)
    return np.array(r, dtype=np.int64) # dim = k

def BitDecompInvMatrix(A: np.ndarray, ell: int, q: int) -> np.ndarray:
    return np.array([BitDecompInvVector(row, ell, q) for row in A], dtype=np.int64)

def FlattenVector(a: np.ndarray, ell: int, q: int) -> np.ndarray: # dim(a) = N = k * ell
    return BitDecompVector(BitDecompInvVector(a, ell, q), ell, q) # dim = N = k * ell

def FlattenMatrix(A: np.ndarray, ell: int, q: int) -> np.ndarray:
    return BitDecompMatrix(BitDecompInvMatrix(A, ell, q), ell, q)

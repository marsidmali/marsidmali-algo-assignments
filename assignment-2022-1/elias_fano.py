import hashlib
import math
import sys


def elias_fano(lst):
    m, n = max(lst), len(lst)
    l = math.floor(math.log2(m/n))
    L, U = bytearray(math.ceil(n * l)), bytearray(n + math.ceil((m / (2 ** l))))
    prev_n, j, k, L_byte_len, U_byte_len = 0, 0, 0, 8, 8
    for i in lst:
        lower_bits, higher_bits = i & ((1 << l) - 1), i >> l
        dif, prev_n, r = higher_bits - prev_n, higher_bits, l
        while r > 0:
            s = (1 << r - 1) & lower_bits
            while s > 1:
                s = 1
            L[j] = L[j] | (s * (1 << (L_byte_len - 1)))
            L_byte_len -= 1
            while L_byte_len == 0:
                L_byte_len = 8
                j += 1
            r -= 1
        n = 0
        while n < dif:
            U_byte_len -= 1
            n += 1
            if U_byte_len == 0:
                U_byte_len = 8
                k += 1
        U[k] = (U[k] | (1 << (U_byte_len - 1)))
        U_byte_len -= 1
        if U_byte_len == 0:
            U_byte_len = 8
            k += 1
    [L.remove(j) for j in [i for i in L if i == 0]], [U.remove(j) for j in [i for i in U if i == 0]]
    return l, L, U


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        (l, L, U), h = elias_fano([int(x) for x in f.read().split()]), hashlib.sha256()
        print("l", l), print("L"), [print('{:08b}'.format(i)) for i in L], print("U"), [print('{:08b}'.format(i)) for i in U]
        h.update(L), h.update(U), print(h.hexdigest())

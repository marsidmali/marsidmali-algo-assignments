import argparse


def compare(a, b):
    return match if a == b else diff


def enumerate_alignments(a, b, f, w, z):
    i = len(a)
    j = len(b)

    if i == 0 and j == 0:
        ww.append(w)
        zz.append(z)
    if i > 0 and j > 0:
        md = compare(a[i - 1], b[j - 1])
        if f[i][j] == f[i - 1][j - 1] + md:
            enumerate_alignments(*(a[:i - 1], b[:j - 1], f, [a[i - 1]] + w, [b[j - 1]] + z) if l else (a[:i - 1], b[:j - 1], f, a[i - 1] + w, b[j - 1] + z))
    if i > 0 and f[i][j] == f[i - 1][j] + gap:
        enumerate_alignments(*(a[:i - 1], b, f, [a[i - 1]] + w, ["-"] + z) if l else (a[:i - 1], b, f, a[i - 1] + w, "-" + z))
    if j > 0 and f[i][j] == f[i][j - 1] + gap:
        enumerate_alignments(*(a, b[:j - 1], f, ["-"] + w, [b[j - 1]] + z) if l else (a, b[:j - 1], f, "-" + w, b[j - 1] + z))
    return ww, zz


def needlemanwunsch(a, b):
    f = [[0 for _ in range(len(b) + 1)] for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        f[i][0] = i * gap
    for j in range(len(b) + 1):
        f[0][j] = j * gap
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            md = compare(a[i - 1], b[j - 1])
            f[i][j] = max(f[i - 1][j] + gap, f[i][j - 1] + gap, f[i - 1][j - 1] + md)
    global ww, zz
    ww, zz = [], []
    ww, zz = enumerate_alignments(a, b, f, [] if l else "", [] if l else "")
    return ww, zz


def compute_alignment_score(A, B):
    l, k = [], []
    for i in range(len(B) + 1):
        l.append(i * gap)
        k.append(0)
    for i in range(1, len(A) + 1):
        l, k = k, l
        l[0] = i * gap
        for j in range(1, len(B) + 1):
            md = compare(A[i - 1], B[j - 1])
            l[j] = max(l[j - 1] + gap, k[j] + gap, k[j - 1] + md)
    return l


def update_alignments(ww, zz, wwl, wwr, zzl, zzr):
    for i, j in zip(wwl, zzl):
        for k, l in zip(wwr, zzr):
            ww.append(i + k)
            zz.append(j + l)


def hirschberg(a, b):
    if len(a) == 0:
        ww = ['-' * len([b] if l else b)]
        zz = [b]
    elif len(b) == 0:
        ww = [a]
        zz = ['-' * len([a] if l else a)]
    elif len([a] if l else a) == 1 or len([b] if l else b) == 1:
        ww, zz = needlemanwunsch(a, b)
    else:
        i = len(a) // 2
        sl = compute_alignment_score(a[:i], b)
        sr = compute_alignment_score(a[i:][::-1], b[::-1])
        s = [m + n for m, n in zip(sl, sr[::-1])]
        j_ = [x for x in range(len(s)) if s[x] == max(s)]
        ww, zz = [], []
        for j in j_:
            if t:
                print(f"{i}, {j}")
            wwl, zzl = hirschberg(a[:i], b[:j])
            wwr, zzr = hirschberg(a[i:], b[j:])
            update_alignments(ww, zz, wwl, wwr, zzl, zzr)
    return ww, zz


def print_alignments():
    if args.f:
        with open(args.seq1, 'r') as a, open(args.seq2, 'r') as b:
            if args.l:
                a = a.read().splitlines()
                b = b.read().splitlines()
                for w, z in zip(*hirschberg(a, b)):
                    for i, j in zip(w, z):
                        if i == j:
                            print(f"= {i}\n= {j}")
                        else:
                            print(f"< {i}\n> {j}")
    else:
        a = []
        for i in zip(*hirschberg(args.seq1, args.seq2)):
            if i not in a:
                a.append(i)
        for w, z in a:
            print(w, f"\n{z}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", action="store_true", help="print i,j")
    parser.add_argument("-f", action="store_true", help="The input is a file")
    parser.add_argument("-l", action="store_true", help="The input sequences are lines")
    parser.add_argument("gap", type=int, help="gap penalty")
    parser.add_argument("match", type=int, help="match")
    parser.add_argument("diff", type=int, help="diff")
    parser.add_argument("seq1", type=str, help="1st sequence to be aligned")
    parser.add_argument("seq2", type=str, help="2nd sequence to be aligned")

    args = parser.parse_args()
    gap = args.gap
    match = args.match
    diff = args.diff
    t = args.t
    l = args.l

    print_alignments()

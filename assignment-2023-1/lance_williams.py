import sys


def calculate_distance(d_sv, d_tv, d_st, s, t, v, method):
    a_i, a_j, b, g = {"single": (0.5, 0.5, 0, -0.5), "complete": (0.5, 0.5, 0, 0.5),
                      "average": (s / (s + t), t / (s + t), 0, 0),
                      "ward": ((s + v) / (s + t + v), (t + v) / (s + t + v), -v / (s + t + v), 0)}[method]
    return a_i * d_sv + a_j * d_tv + b * d_st + g * abs(d_sv - d_tv)


def lance_williams(clusters, method):
    n = len(clusters)
    distance_matrix = [[abs(clusters[i][0] - clusters[j][0]) for j in range(n)] for i in range(n)]

    while n > 1:
        dist, (s, t) = min((distance_matrix[i][j], (i, j)) for i in range(n) for j in range(i + 1, n))
        n_s, n_t = len(clusters[s]), len(clusters[t])
        print(f"({' '.join(map(str, clusters[s]))}) ({' '.join(map(str, clusters[t]))}) {dist:.2f} {n_s + n_t}")
        clusters[s] += clusters[t]

        for v in range(n):
            if v not in (s, t):
                d_sv = distance_matrix[s][v]
                d_tv = distance_matrix[t][v]
                d_st = distance_matrix[s][t]
                n_v = len(clusters[v])
                distance_matrix[s][v] = distance_matrix[v][s] = calculate_distance(d_sv, d_tv, d_st, n_s, n_t, n_v, method)

        for i in range(len(distance_matrix)):
            del distance_matrix[i][t]
        del distance_matrix[t]

        clusters.pop(t)
        n -= 1


if __name__ == "__main__":
    with open(sys.argv[2], 'r') as f:
        clusters_, method_ = sorted([[int(c)] for c in (f.read().split())]), sys.argv[1]
    lance_williams(clusters_, method_)

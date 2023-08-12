from sys import argv
from collections import deque


def lex_bfs(graph):
    # Φτιάχνουμε μία λίστα Σ η οποία περιέχει ένα σύνολο με όλους τους κόμβους του γράφου
    S = deque([set(graph.keys())])
    lex_order = []
    # Όσο η λίστα Σ δεν είναι άδεια
    while S:
        u = min(S[0])
        # Αφαιρούμε έναν κόμβο 𝑢 από το πρώτο σύνολο της Σ
        S[0].remove(u)
        # Προσθέτουμε τον 𝑢 στη λεξικογραφική κατά πλάτος διάταξη
        lex_order.append(u)
        # Αν το πρώτο σύνολο της Σ αδειάσει, το αφαιρούμε από τη Σ
        if not S[0]:
            S.popleft()
        # Στο SS συλλέγουμε τα SSn στα οποία συλλέγουμε όλους τους γείτονες του 𝑢 που ανήκουν στα Σ𝑣
        SS = {i: set() for i in range(len(S))}
        # Για κάθε έναν γείτονα 𝑣 του 𝑢
        for v in graph[u]:
            # που δεν έχουμε επισκεφτεί ακόμα
            if v not in lex_order:
                for Sn, SSn in zip(S, SS.values()):
                    # Έστω ότι Sn είναι το σύνολο στο οποίο ανήκει ο 𝑣
                    if v in Sn:
                        # Αφαιρούμε τον 𝑣 από το Sn
                        Sn.remove(v)
                        # Τον προσθέτουμε στο σύνολο SSn
                        SSn.add(v)
                        # Αν το Sn άδειασε, το αφαιρούμε απο τη Σ
                        if not Sn:
                            S.remove(Sn)
                        break
        # Εισάγουμε τα SSns πριν από τα Sns στη Σ
        for n, SSn in sorted(SS.items(), reverse=True):
            # Εισάγουμε μόνο τα μη κενά(αχρησιμοποίητα) SSns
            if SSn:
                S.insert(n, SSn)
    # Επιστρέφουμε τη λεξικογραφική κατά πλάτος σειρά με την οποία επισκεφτήκαμε τους κόμβους
    return lex_order


def is_chordal(graph):
    # Αντίστροφη λεξικογραφική κατά πλάτος διάταξη
    reverse_lex_order = lex_bfs(graph)[::-1]
    # Για κάθε κόμβο 𝑢 σε αντίστροφη λεξικογραφική κατά πλάτος διάταξη
    for u in reverse_lex_order:
        # Έστω RN(𝑢) οι γείτονες του 𝑢 που έπονται του 𝑢 στην αντίστροφη λεξικογραφική κατά πλάτος διάταξη
        RNu = {i for i in graph[u] if reverse_lex_order.index(i) > reverse_lex_order.index(u)}
        if RNu:
            # Έστω 𝑣 ο πρώτος γείτονας του 𝑢 στην αντίστροφη λεξικογραφική κατά πλάτος διάταξη
            v = min(RNu, key=reverse_lex_order.index)
            # RN(𝑣) οι γείτονες του 𝑣 που έπονται του 𝑣 στην αντίστροφη λεξικογραφική κατά πλάτος διάταξη.
            RNv = {j for j in graph[v] if reverse_lex_order.index(j) > reverse_lex_order.index(v)}
            # Αν RΝ(𝑢) ⧵ {𝑣} ⊈ RN(𝑣), τότε ο γράφος δεν είναι χορδικός, και σταματάμε
            if not (RNu - {v}).issubset(RNv):
                return False
    return True


def connected_component(graph, u, v):
    # Αφαιρούμε κάθε έναν κόμβο 𝑢 και τους γείτονες του από τον G
    g_nu = {node: (v - {u} - graph[u]) for node, v in graph.items() if node != u}
    queue, visited = deque([v]), set()
    visited.add(v)
    # Βρίσκουμε, χρησιμοποιώντας την απλή κατά πλάτος αναζήτηση, τις συνιστώσες που προκύπτουν από τον 𝐺 ⧵ 𝑁 (𝑢)
    while queue:
        node = queue.popleft()
        for neighbor in g_nu[node]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
    return visited


def is_asteroidal_triple_free(graph):
    # Αρχικοποιούμε έναν πίνακα 𝐶 διαστάσεων |𝑉|×|𝑉|
    C = [[0 for i in range(len(graph))] for i in range(len(graph))]
    # όπου στο κελί 𝑢, 𝑣 του 𝐶
    for u in graph:
        for v in graph:
            # βάζουμε τη συνιστώσα του 𝐺 ⧵ 𝑁 (𝑢) στην οποία ανήκει ο κόμβος 𝑣 αν οι κόμβοι 𝑢 και 𝑣 δεν είναι γείτονες
            if v not in graph[u] and u != v:
                C[u][v] = connected_component(graph, u, v)
    # Για να μην έχει ο γράφος αστεροειδείς τριπλέτες, θα πρέπει για καμία τριπλέτα 𝑢, 𝑣, 𝑤
    for u in range(len(C)):
        for v in range(u + 1, len(C)):
            for w in range(v + 1, len(C)):
                # έλεγχος μόνο μη μηδενικών κελιών
                if all(c != 0 for c in [C[u][v], C[u][w], C[w][v]]):
                    # να μην ισχύει 𝐶[𝑢, 𝑣] = 𝐶[𝑢, 𝑤], 𝐶[𝑣, 𝑢] = 𝐶[𝑣, 𝑤], 𝐶[𝑤, 𝑢] = 𝐶[𝑤, 𝑣]
                    if C[u][v] == C[u][w] and C[v][u] == C[v][w] and C[w][u] == C[w][v]:
                        return False
    return True


if __name__ == '__main__':
    graph_ = {}
    with open(argv[2], 'r') as file:
        for line in file:
            v, e = map(int, line.strip().split())
            graph_.setdefault(v, set()).add(e)
            graph_.setdefault(e, set()).add(v)

    if argv[1] == "lexbfs":
        print(lex_bfs(graph_))
    elif argv[1] == "chordal":
        print(is_chordal(graph_))
    elif argv[1] == "interval":
        print(is_chordal(graph_) and is_asteroidal_triple_free(graph_))

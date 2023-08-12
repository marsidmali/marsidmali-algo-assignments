import argparse
from collections import deque


class Node:
    number_of_nodes = 0

    def __init__(self, parent=None):
        self.node_number = Node.number_of_nodes
        self.parent = parent
        self.children = {}
        self.depth = 0
        self.is_terminal = False
        Node.number_of_nodes += 1


class Trie:
    def __init__(self):
        self.root = Node()
        # Το λεξικό nodes στο οποίο αποθηκεύουμε τους κόμβους του Trie μας "γλιτώνει" απο την ανάγκη υλοποίησης κατά
        # πλάτος αναζήτησης κάθε φόρα όπου θέλουμε να διατρέξουμε τους κόμβους του Trie. Επίσης, με τον αριθμό ενός
        # κόμβου(node_number) μέσω του λεξικού μπορούμε να ανακτήσουμε τον ίδιο τον κόμβο με υπολογιστικό κόστος Ο(1).
        self.nodes = {self.root.node_number: self.root}

    def insert(self, keyword):
        # Αρχικοποιούμε τον κόμβο με τη ρίζα του Trie
        node = self.root
        # Διασχίζουμε τον όρο αναζήτησης
        for char in keyword:
            # Εάν ο χαρακτήρας δεν υπάρχει στα παιδιά του κόμβου
            if char not in node.children:
                # Δημιουργούμε νέο κόμβο Node
                new_node = Node(parent=node)
                # Ως παιδί του τρέχοντος κόμβου
                node.children[char] = new_node
                # Αποθηκεύουμε τον κόμβο στο λεξικό nodes με κλειδί τον αριθμό του
                self.nodes[new_node.node_number] = new_node
            # Μεταβαίνουμε στον επόμενο κόμβο
            node = node.children[char]
            # Ορίζουμε το βάθος του κόμβου σε σχέση με τον γονέα του
            node.depth = node.parent.depth + 1
        # Σημειώνουμε τον τελικό κόμβο ως τερματικό
        node.is_terminal = True

    def print_trie(self, node=None, indent='', last=True, path='', s1=None, s2=None):
        if node is None:
            node = self.root

        print(indent, end='')
        if node == self.root:
            print('', end='')
            indent += ''
        elif last:
            print('\033[93m    `-- \033[0m', end='')
            indent += '\033[93m       \033[0m'
        else:
            print('\033[93m   |--- \033[0m', end='')
            indent += '\033[93m   |  \033[0m'

        if node == self.root:
            print(f'\033[38;5;208;1m({node.node_number}: \033[93m{s1[node.node_number]},{s2[node.node_number]}\033[0m\033[38;5;208;1m)')
        elif node.is_terminal:
            print(f'\033[38;5;208;1m({node.node_number}: \033[93m{s1[node.node_number]},{s2[node.node_number]}\033[0m\033[38;5;208;1m)\033[0m  \033[93m-->\033[0m \033[92m{path}\033[0m  --  \033[94m{path[::-1]}\033[0m')
        else:
            print(f'\033[38;5;208;1m({node.node_number}: \033[93m{s1[node.node_number]},{s2[node.node_number]}\033[0m\033[38;5;208;1m)\033[0m \033[93m-->\033[0m \033[92m{path}\033[0m')

        if node.children:
            sorted_keys = sorted(node.children.keys())
            for i, key in enumerate(sorted_keys):
                child = node.children[key]
                is_last = i == len(sorted_keys) - 1
                self.print_trie(child, indent, is_last, path + key, s1, s2)


class CommentzWalter:
    def __init__(self, keywords, text):
        self.trie = Trie()
        self.keywords = keywords
        self.text = text
        self.pmin = min(len(word) for word in self.keywords)
        self.failure_table = {}
        self.s1 = {}
        self.s2 = {}
        self.rt = {}

    def build_failure_table(self):
        # Θέτουμε failure[𝑢] ← 0 για κάθε κόμβο 𝑢 σε βάθος 𝑑 ≤ 1 του trie
        self.failure_table = {u: 0 for u, u_node in self.trie.nodes.items() if u_node.depth <= 1}
        #  Διατρέχουμε το trie με μία κατά πλάτος αναζήτηση
        queue = deque(self.trie.root.children.values())
        while queue:
            # Για κάθε κόμβο 𝑢 που επισκεπτόμαστε στην κατά πλάτος αναζήτηση εξετάζουμε ένα-ένα τα παιδιά του
            u = queue.popleft()
            # Για κάθε παιδί 𝑣 που συνδέεται με τον 𝑢 με έναν σύνδεσμο 𝑐
            for c, v in u.children.items():
                # Θέτουμε 𝑢𝑢 ← failure[𝑢]
                uu = self.failure_table[u.node_number]
                # Όσο ο κόμβος 𝑢𝑢 στο trie δεν έχει παιδί με σύνδεσμο 𝑐, και ο 𝑢𝑢 δεν είναι η ρίζα
                while c not in self.trie.nodes[uu].children and uu != 0:
                    # θέτουμε 𝑢𝑢 ← failure[𝑢𝑢]
                    uu = self.failure_table[uu]
                # Αν βρήκαμε πρόγονο κόμβο 𝑢𝑢 με παιδί 𝑣𝑣 μέσω συνδέσμου 𝑐
                if c in self.trie.nodes[uu].children:
                    vv = self.trie.nodes[uu].children[c]
                    # Θέτουμε failure[𝑣] ← 𝑣𝑣
                    self.failure_table[v.node_number] = vv.node_number
                else:
                    # Διαφορετικά, θέτουμε failure[𝑣] ← 0
                    self.failure_table[v.node_number] = 0
                queue.append(v)

    def construct_s1_s2(self):
        # set1[𝑢] = {𝑣 ∶ failure[𝑣] = 𝑢}
        set1 = {u: {v for v, uu in self.failure_table.items() if uu == u} for u in range(len(self.failure_table))}
        # set2[𝑢] = {𝑣 ∶ 𝑣 ∈ set1[𝑢] και ο 𝑣 είναι τερματικός κόμβος στο trie
        set2 = {u: {v for v in set1[u] if self.trie.nodes[v].is_terminal} for u in set1.keys()}
        # Διατρέχουμε τους κόμβους του trie μέσω του nodes λεξικού(αντί να διατρέξουμε το trie με κατά πλάτος αναζήτηση)
        for u, u_node in self.trie.nodes.items():
            if u_node == self.trie.root:
                self.s1[u] = 1          # 𝑠1[𝑢] = 1,    για 𝑢 = 𝑟
                self.s2[u] = self.pmin  # 𝑠2[𝑢] = pmin, για 𝑢 = 𝑟
            else:
                k_1 = [self.trie.nodes[uu].depth - u_node.depth for uu in set1[u]]
                # 𝑠1[𝑢] = min{pmin, 𝑘 ∶ 𝑘 = 𝑑(𝑢′) − 𝑑(𝑢), 𝑢′∈ set1[𝑢]} για 𝑢 ≠ 𝑟
                self.s1[u] = min(self.pmin, *k_1) if k_1 else self.pmin
                k_2 = [self.trie.nodes[uu].depth - u_node.depth for uu in set2[u]]
                parent_u = u_node.parent.node_number
                # 𝑠2[𝑢] = min{𝑠2[parent(𝑢)], 𝑘 ∶ 𝑘 = 𝑑(𝑢′) − 𝑑(𝑢), 𝑢′∈ set2[𝑢]} για 𝑢 ≠ 𝑟
                self.s2[u] = min(self.s2[parent_u], *k_2) if k_2 else self.s2[parent_u]

    def has_child(self, u, character):
        return character in self.trie.nodes[u].children

    def get_child(self, u, character):
        return self.trie.nodes[u].children[character].node_number

    def is_terminal(self, u):
        return self.trie.nodes[u].is_terminal

    def built_rt(self):
        # Συμπεριλαμβάνουμε όλους τους ASCII χαρακτήρες
        ascii_chars = "".join([chr(i) for i in range(128)])
        # Αρχικοποιούμε τον πίνακα με την τιμή που θα λάβουν οι χαρακτήρες που δεν υπάρχουν στους όρους αναζήτησης
        self.rt = {char: self.pmin + 1 for char in ascii_chars}
        # Διατρέχουμε τους κόμβους του trie μέσω του nodes λεξικού(αντί να διατρέξουμε το trie με κατά πλάτος αναζήτηση)
        for u in self.trie.nodes.values():
            # Διατρέχουμε τα παιδιά του κόμβου u
            for char, uu in u.children.items():
                # Ενημερώνουμε το ελάχιστο βάθος για κάθε χαρακτήρα rt[char] = min(pmin + 1, {𝑑(𝑢) ∶ 𝑙(𝑢) = char})
                self.rt[char] = min(self.rt[char], uu.depth)

    def commentz_walter(self, t):
        q = deque()
        i = self.pmin - 1
        j = 0
        u = 0
        m = ''
        while i < len(t):
            while self.has_child(u, t[i - j]):
                u = self.get_child(u, t[i - j])
                m += t[i - j]
                j += 1
                if self.is_terminal(u):
                    q.append((m[::-1], i - j + 1))
            if j > i:
                j = i
            s = min(self.s2[u], max(self.s1[u], self.rt[t[i - j]] - j - 1))
            i += s
            j = 0
            u = 0
            m = ''
        return q

    def run(self):
        # Εισάγουμε τους όρους αναζήτησης ανεστραμμένους στο Trie
        for k in self.keywords:
            self.trie.insert(k[::-1])
        # Δημιουργούμε τον πίνακα failure
        self.build_failure_table()
        # Δημιουργούμε τον πίνακα rt
        self.built_rt()
        # Δημιουργούμε τα s1, s2
        self.construct_s1_s2()
        # Εάν έχει δοθεί το optional argument -v εμφανίζουμε τα περιεχόμενα των s1,s2 και τον κόμβο που εντοπίζονται
        if args.v:
            for (node, s1_content), s2_content in zip(self.s1.items(), self.s2.values()):
                print(f"{node}: {s1_content},{s2_content}")
        if args.t:
            self.trie.print_trie(s1=self.s1, s2=self.s2)
        # Εμφανίζουμε τους όρους αναζήτησης καθώς και τη θέση στην οποίο εντοπίζονται στο κείμενο
        for keyword, position in self.commentz_walter(self.text):
            print(f"{keyword}: {position}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", action="store_true", help="display contents of s1 and s2 for each node")
    parser.add_argument("-t", action="store_true", help="print trie and the contents of s1 and s2 for each node")
    parser.add_argument("kw", nargs="+", help="keywords")
    parser.add_argument("input_filename", type=argparse.FileType('r'), help="txt file")
    args = parser.parse_args()

    cw = CommentzWalter(args.kw, args.input_filename.read())
    cw.run()

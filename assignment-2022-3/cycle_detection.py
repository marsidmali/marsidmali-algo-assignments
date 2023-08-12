import argparse


class CycleDetection:
    def __init__(self, b, g, max_size, table, d):
        self.b = b
        self.g = g
        self.max_size = max_size
        self.table = table
        self.d = d

    def f(self, x):
        return self.d[x]

    def insert_in_table(self, table, y, i):
        table.update({y: i})

    def purge(self, table, b):
        pop = [i for i, j in table.items() if (j % 2 * b) != 0]        
        for x in pop:                                                  
            table.pop(x)

    def search_table_y(self, table, y):
        if y in table.keys():                      
            return table[y]
        else:
            return -1

    def search_table_j(self, table, k):
        if k in table.values():                     
            return list(table.keys())[list(table.values()).index(k)]
        else:
            return -1

    def fk(self, k):
        kb = self.search_table_j(self.table, self.b * (k // self.b))
        if kb != -1:                                
            for n in range(k % self.b):             
                kb = self.f(kb)
        return kb

    def detect_cycle(self, x):
        y = x
        i = 0
        m = 0
        while True:
            if i % self.b == 0 and m == self.max_size:
                self.b = 2 * self.b
                self.purge(self.table, self.b)
                m = m // 2
            if i % self.b == 0:
                self.insert_in_table(self.table, y, i)
                m = m + 1
            y = self.f(y)
            i = i + 1
            if (i % (self.g * self.b)) < self.b:
                j = self.search_table_y(self.table, y)
                if j != -1:
                    return y, i, j
    
    def recover_cycle(self, y, i, j):
        c = 1
        found_c = False
        yc = y
        while c <= ((self.g + 1) * self.b) and found_c is False:
            yc = self.f(yc)
            if y == yc:
                found_c = True
            else:
                c = c + 1
        if found_c is False:
            c = i - j
        block_lenght = self.g * self.b
        final_block = block_lenght * (i // block_lenght)
        previous_block = final_block - block_lenght
        ii = max(c, previous_block)
        jj = ii - c
        l = jj + 1
        while self.fk(l) != self.fk(l + c):
            l = l + 1
        return c, l

    def print_results(self, c, l):
        print("cycle", c, "leader", l)
        if t:
            sortable = dict(sorted(self.table.items()))    
            for i, j in sortable.items():      
                print(i, j)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", action="store_true", help="print table")
    parser.add_argument("b", type=int, help="a positive integer")
    parser.add_argument("g", type=int, help="a positive integer")
    parser.add_argument("table_size", type=int, help="table max_size")
    parser.add_argument("input_sequence", type=argparse.FileType('r'), help="txt file")

    args = parser.parse_args()
    b = args.b
    g = args.g
    max_size = args.table_size
    t = args.t
    file = args.input_sequence.readlines()
    
    d = {}                                              
    j = 1                                               
    for i in file:                                      
        if j < len(file):                               
            d[int(i)] = int(file[j])                   
        j = j + 1                                       
    
    cd = CycleDetection(b, g, max_size, {}, d)
    y, i, j = cd.detect_cycle(int(file[0]))
    c, l = cd.recover_cycle(y, i, j)
    cd.print_results(c, l)

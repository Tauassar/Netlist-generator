def dfs_iterative(graph, start):
    stack, path = [start], []

    while stack:
        vertex = stack.pop()
        if vertex in path:
            continue
        path.append(vertex)
        for neighbor in graph[vertex]:
            stack.append(neighbor)

    return path


adjacency_matrix = {'A': ['B', 'C'], 'B': ['D', 'E'],
                    'C': ['E'], 'D': ['F'], 'E': ['F'],
                    'F': ['G'], 'G': []}

print(dfs_iterative(adjacency_matrix, 'A'))


def countpath(self, x, neighbors):
    temp1 = []
    temp2 = []
    counter = 0
    self.pathses[counter].append(x)
    l = len(neighbors)
    if l == 1:
        counter = counter + 1
    elif l >= 3:
        while l >= 3:
            l = l - 1
            a = counter
            while (True):
                try:
                    print('A ', a)
                    if self.pathses[a + 2] != None and self.pathses[a + 1] != None:
                        break
                    temp1 = self.pathses[a].copy()
                    temp2 = self.pathses[a + 1]
                    a = a + 1
                except(IndexError):
                    self.pathses.append([])

    node1=Node('FF1', 'FF', 3, 5, 1, True)
    node2=Node('AND1', 'GATE', 2)
    node3=Node('OR1', 'GATE', 3)
    node4=Node('OR2', 'GATE', 3)
    node5=Node('FF2', 'FF', 3, 5, 1)
    node6=Node('FF3', 'FF', 3, 5, 1)

    myCircuit=netlist()
    myCircuit.add(node1, node2)
    myCircuit.add(node2, node3, node4)
    myCircuit.add(node3, node5)
    myCircuit.add(node4, node6)
    myCircuit.timingAnalyze()
'''
    def adj_matrix(self,inp:list):
        out=[]
        for x in inp:
            adjacency_matrix={}
            for node in self.nodes:
                if node.getnodeName() in inp and node.getnodeName()!=x:
                    continue
                adjacency_matrix[node.getnodeName()]=list(self.g.neighbors(node.getnodeName()))
            adjacency_matrix=self.delOld(adjacency_matrix,inp,node.getnodeName())
            out.append(adjacency_matrix)
        return out
'''

'''adjacency_m = {}


def matrix(self, x, inp, z):
    if x in inp and x != z:
        return
    if x in self.adjacency_m:
        return
    neigh = list(self.g.neighbors(x))
    self.adjacency_m[x] = neigh
    for neighbors in neigh:
        try:
            self.adjacency_m.update(self.matrix(neighbors, inp, z))
        except:
            print(end='')
    return self.adjacency_m


def adj_matrix(self, inp: list):
    out = []
    for x in inp:
        self.adjacency_m.clear()
        adjacency_matrix = self.matrix(x, inp, x)
        adjacency_matrix = self.delOld(adjacency_matrix, inp, x)
        out.append(adjacency_matrix)
    return out'''
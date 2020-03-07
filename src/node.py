import matplotlib.pyplot as plt
import networkx as nx

class Node:
    nodeName=''
    type='';
    propDelay=0
    setupT=None
    holdT=None
    isInp=False
    def __init__(self,a,b,c,d=None,e=None,f=False):
        self.nodeName = a
        self.type=b
        self.propDelay = c
        self.setupT = d
        self.holdT = e
        self.isInp=f

    def isInput(self):
        return self.isInp
    def getSetupT(self):
        return self.setupT
    def getHold(self):
        return self.holdT
    def getPropagation(self):
        return self.propDelay
    def getnodeName(self):
        return self.nodeName
    def getType(self):
        return self.type

class netlist:
    nodeslist={};
    input_nodes=[]
    g = nx.Graph()
    nodes=[]

    def drawThing(self):
        FF_nodes=[]
        inputs=[]
        FF_inp=[]
        gate_inp=[]
        gate_nodes=[]
        size=600
        for node in self.input_nodes:
            inputs.append(node.getnodeName())
        for x in self.nodeslist:
            if x in inputs:
                if self.nodeslist[x]=='FF':
                    FF_inp.append(x)
                else:
                    gate_inp.append(x)
            if self.nodeslist[x]=='FF':
                FF_nodes.append(x)
            else:
                gate_nodes.append(x)

        pos = nx.spring_layout(self.g,k=0.3)
        nx.draw_networkx_nodes(self.g, pos,  node_size = size, nodelist=gate_nodes, \
                               node_color='blue', node_shape='o')
        nx.draw_networkx_nodes(self.g, pos,  node_size = size, nodelist=FF_nodes, \
                               node_color='red', node_shape='s')
        nx.draw_networkx_nodes(self.g, pos,  node_size = size, nodelist=FF_inp, \
                               node_color='green', node_shape='s')
        nx.draw_networkx_nodes(self.g, pos,  node_size = size, nodelist=gate_inp, \
                               node_color='green', node_shape='o')
        nx.draw_networkx_edges(self.g,pos)
        nx.draw_networkx_labels(self.g,pos)
        plt.show()

    def findInputs(self):
        inputs=[]
        for node in self.nodes:
            if node.isInput():
                inputs.append(node)
            else:
                continue
        return inputs


    pathses = [[]]
    curr = 0
    def countpath(self,x,neighbors):
        self.pathses[self.curr].append(x)
        l=len(neighbors)
        if l==0:
            print('\t\tPath ', self.curr+1,' is found\n', self.pathses[self.curr])
            self.curr+=1
        elif l>=2:
            while l!=1:
                self.pathses.insert(self.curr+1,self.pathses[self.curr].copy())
                l-=1

    def add(self, origin, suc1,suc2=None):
        if suc2 is not None:
            self.g.add_nodes_from([origin.getnodeName()])
            self.g.add_nodes_from([suc1.getnodeName(), suc2.getnodeName()])
            self.g.add_edges_from([(origin.getnodeName(), suc1.getnodeName()),(origin.getnodeName(), suc2.getnodeName())])
            self.nodeslist[origin.getnodeName()]=origin.getType()
            self.nodeslist[suc1.getnodeName()]=suc1.getType()
            self.nodeslist[suc2.getnodeName()]=suc2.getType()
            self.nodes.append(origin)
            self.nodes.append(suc1)
            self.nodes.append(suc2)
        else:
            self.g.add_nodes_from([origin.nodeName])
            self.g.add_nodes_from([suc1.nodeName])
            self.g.add_edges_from([(origin.nodeName, suc1.nodeName)])
            self.nodeslist[origin.getnodeName()]=origin.getType()
            self.nodeslist[suc1.getnodeName()]=suc1.getType()
            self.nodes.append(origin)
            self.nodes.append(suc1)

    def adj_matrix(self):
        adjacency_matrix={}
        for node in self.nodes:
            adjacency_matrix[node.getnodeName()]=list(self.g.neighbors(node.getnodeName()))
        adjacency_matrix=self.delOld(adjacency_matrix)
        return adjacency_matrix

    def delOld(self,graph:dict):
        keys=list(graph.keys())
        ln=len(graph)
        tempkeys=[]
        counter=0
        while(True):
            for key in tempkeys:
                if key in graph[keys[counter]]:
                    graph[keys[counter]].remove(key)
            tempkeys.append(keys[counter])
            counter+=1
            ln-=1
            if ln==0:
                break
        return graph

    def dfs_iterative(self, graph, x:Node):
        start=x.getnodeName()
        stack, path = [start], []

        while stack:
            vertex = stack.pop()
            if vertex in path:
                continue
            path.append(vertex)
            try:
                self.countpath(vertex,graph[vertex])
            except(IndexError):
                self.pathses.append([])
                self.countpath(vertex,graph[vertex])
            for neighbor in graph[vertex]:
                stack.append(neighbor)
        return path

    def longPath(self):
        length=None
        longest=[]
        for path in self.pathses:
            if length==None or length<=len(path):
                if length!=None and length<len(path):
                    longest.clear()
                longest.append(path)
                length = len(path)
        print('\nThe longest path: ',longest)
        return longest

    def shortPath(self):
        length=None
        shortest=[]
        for path in self.pathses:
            if length==None or length>=len(path):
                if length!=None and length>len(path):
                    shortest.clear()
                shortest.append(path)
                length = len(path)
        print('\nThe shortest path: ',shortest)
        return shortest

    def findNode(self, x:str):
        for node in self.nodes:
            if x==node.getnodeName():
                return node
        print(x,' is not found!')

    def calcPathdelay(self, path:list):
        Ts=0
        for element in path:
            node = self.findNode(element)
            if node.getType() == 'FF':
                if node.isInput() == True:
                    Ts += node.getPropagation()
                    continue
                else:
                    Ts += node.getSetupT()
                    continue
            else:
                Ts += node.getPropagation()
        return Ts


    def findFmax(self, list):
        Ts=[]
        comboMax=0
        for path in list:
            first=self.findNode(path[0])
            second = self.findNode(path[-1])
            if first.getType()!='FF' or second.getType()!='FF':
                combo=self.calcPathdelay(path)
                comboMax=combo if combo>comboMax else comboMax
            else:
                Ts.append(self.calcPathdelay(path))

        if len(Ts)!=0:
            Tsmax=max(Ts)
            print('\nTs(max) is equal to', Tsmax)
            return 1 / Tsmax
        else:
            print('\nThe path is purely combinational, Combo max is ', comboMax)
            return 1/comboMax

    def constraint(self, path: list):
        Ts = 0
        lastNode=self.findNode(path.pop(-1))
        for element in path:
            node = self.findNode(element)
            if node.getType() == 'FF':
                Ts += node.getPropagation()
            else:
                Ts += node.getPropagation()
        if lastNode.getHold()<=Ts:
            return True
        else:
            return False


    def hold_time_constraint(self, list):
        comboMin=0
        minVal=[]
        for path in list:
            first=self.findNode(path[0])
            second = self.findNode(path[-1])
            if first.getType()!='FF' or second.getType()!='FF':
                continue
            else:
                minVal.append(self.constraint(path))
        if len(minVal)!=0:
            for val in minVal:
                if val==False:
                    return False
            return True
        print("hold time constraint cannot be calculated, the path is purely combinational")


    def timingAnalyze(self):
        self.nodes = list(dict.fromkeys(self.nodes)) #remove duplicate nodes
        print('\t\t\t\tFinding input nodes...')
        self.input_nodes=self.findInputs()
        var=[self.input_nodes[i].getnodeName() for i in range(len(self.input_nodes))]
        print('input nodes:', var, sep=' ')
        adj_matrix=self.adj_matrix()
        print('\n\t\t\tFinding pathses...')
        for x in self.input_nodes:
            self.dfs_iterative(adj_matrix,x)
        longest=self.longPath()
        shortest = self.shortPath()
        print("Fmax is equal to ", self.findFmax(longest))
        msg="\n\t\tHold time constraint is satisfied, no clock skew is needed" if self.hold_time_constraint(shortest) else "\n\t\t\t\tHold time constraint is not satisfied, clock skew is needed"
        print(msg)
        print('\n\t\t\t\tDrawing schematic of your circuit...')
        self.drawThing()

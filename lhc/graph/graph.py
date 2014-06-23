from collections import defaultdict

class Graph(object):
    def __init__(self, name=None):
        self.name = 'G' if name is None else name
        self.vs = {}
        self.es = defaultdict(set)
        
    def __str__(self):
        res = ['digraph %s {'%self.name]
        for v1, es in self.vs.iteritems():
            for e, v2 in es.iteritems():
                res.append('    %s -> %s [label="%s"];'%(v1, v2, e))
        res.append('}')
        return '\n'.join(res)
    
    def addVertex(self, v):
        if v not in self.vs:
            self.vs[v] = {}
    
    def addEdge(self, e, v1, v2=None):
        self.vs[v1][e] = v2
        self.es[e].add((v1, v2))

    def getParents(self, v):
        res = set()
        for parent, edges in self.vs.iteritems():
            if v in edges.values():
                res.add(parent)
        return res
        
    def getChildren(self, v):
        return self.vs[v].items()

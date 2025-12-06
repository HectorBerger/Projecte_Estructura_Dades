import copy
import math

class GrafHash:
    """Graf amb Adjacency Map structure"""

    class Vertex:
        __slots__ = '_valor'

        def __init__(self, x):
            self._valor=x
                  
        def __str__(self):
            return str(self._valor)
    
################################Definicio Class _Vertex       
    
    def __init__(self, ln=None, lv=None, lp=None, digraf=False):
        """Crea graf (no dirigit per defecte, digraf si dirigit es True.
        """
        if ln is None: ln = []
        if lv is None: lv = []
        if lp is None: lp = []
        
        self._nodes = {}
        self._out = { }
        self._in={} if digraf else self._out
        #nodes={}
        for n in ln:
            v=self.insert_vertex(n)
            #nodes[n]=v
        if lp==[]:
            for v in lv:
                self.insert_edge(v[0],v[1])
        else:
            for vA,pA in zip(lv,lp):
                self.insert_edge(vA[0],vA[1],pA)
    
    def es_digraf(self):
        return self._out!=self._in
    
    def getOut(self):
        return self._out
        
    def insert_vertex(self, x):
        v= self.Vertex(x)
        self._nodes[x] = v
        self._out[x] = { }
        if self.es_digraf():
            self._in[x] = {}
       
        return v

    def insert_edge(self, n1, n2, p1=1):
        
        self._out[n1][n2] = p1
        self._in[n2][n1] = p1
        
    def grauOut(self, x):
        return len(self._out[x])

    def grauIn(self, x):
        return len(self._in[x])
    
    def vertices(self):
        """Return una iteracio de tots els vertexs del graf."""
        return self._nodes.__iter__( )

    def edges(self,x):
        """Return una iteracio de tots els nodes veins de sortida de x al graf."""
        #return self._out[x].items()
        return iter(self._out[x].__iter__())
    
    
    def minDistance(self,dist, visitat):
        minim = math.inf
        res = ""
        for node,distancia in dist.items():
            if node not in visitat and distancia<minim:
                minim = distancia
                res = node
            
        return res


       
    def dijkstra(self,n):
        dist = {nAux:math.inf for nAux in self._out} # node : dist_acum
        predecesors = dict() # node : node_anterior
        visitat = dict() #node : bool
        dist[n] = 0

        for count in range(len(self._nodes)-1):
            u = self.minDistance(dist, visitat)
            visitat[u] = True

            if u in self._out:
                for v,p in self._out[u].items():
                    if v not in visitat:
                        if dist[u] + p < dist[v]:
                            dist[v] = dist[u] + p
                            predecesors[v] = u

        return dist, predecesors


    def dijkstraModif(self,n1,n2):        
        dist = {nAux:math.inf for nAux in self._out} # node : dist_acum
        predecesors = {nAux:None for nAux in self._out} # node : node_anterior
        visitat = dict() #node : bool
        dist[n1] = 0

        count = 0
        while count < len(self._nodes)-1 :
            count += 1
            u = self.minDistance(dist, visitat)
            visitat[u] = True

            if u==n2: break
            elif u in self._out:
                for v,p in self._out[u].items():
                    if v not in visitat:
                        if dist[u] + p < dist[v]:
                            dist[v] = dist[u] + p
                            predecesors[v] = u

        return dist, predecesors
        
    def camiMesCurt(self,n1, n2):
        camicurt = []
        if n1 in self._nodes and n2 in self._nodes:
            dist, predecesors = self.dijkstra(n1)

            if n2 in predecesors:
                camicurt = [n2]
                
                while not n2 == n1:
                    n2 = predecesors[n2]
                    camicurt.append(n2)
                
            camicurt.reverse()
                    
        return camicurt
        
    def __str__(self):
        cad="===============GRAF===================\n"
     
        for it in self._out.items():
            cad1="__________________________________________________________________________________\n"
            cad1=cad1+str(it[0])+" : "
            for valor in it[1].items():
                cad1=cad1+str(str(valor[0])+"("+ str(valor[1])+")"+" , " )
                            
            cad = cad + cad1 + "\n"
        
        return cad
    

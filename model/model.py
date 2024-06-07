import copy

import networkx as nx
from numpy import double

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self.nodi = []
        self.reddito = {}
        self.ricavo = {}
        self.solBest = []

    def buildGraph(self, year, method, s):
        self._grafo.clear()
        self.nodi = DAO.getAllProdotti(method, year)
        self._grafo.add_nodes_from(self.nodi)
        self.addEdgePesati(year, method, s)

    def addEdgePesati(self, year, method, s):
        self._grafo.clear_edges()
        self.ricavo = DAO.getAllProfit(year, method)
        for n1 in self._grafo.nodes:
            for n2 in self._grafo.nodes:
                if n1.Product_number != n2.Product_number:
                    prof1 = self.ricavo[n1.Product_number]
                    prof2 = self.ricavo[n2.Product_number]
                    if prof2 >= (s+1)*double(prof1):
                        self._grafo.add_edge(n1, n2)
                    elif prof1 >= (s+1)*double(prof2):
                        self._grafo.add_edge(n2, n1)

    def getBestPath(self):
        for i in self._grafo.nodes:
            if self._grafo.in_degree(i) == 0:
                parziale = [i]
                self.ricorsione(parziale)
        return self.solBest, self.ricavo

    def ricorsione(self, parziale):
        if self._grafo.out_degree(parziale[-1])==0:
            if len(self.solBest) < len(parziale):
                self.solBest = copy.deepcopy(parziale)

        for n in self._grafo.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self.ricorsione(parziale)
                parziale.pop()


    def getMoreRedditizio(self):
        self.reddito = {}
        for s in self._grafo.nodes:
            #copyright
            #scoperto questo stupendo comando grazie ad ale
            if self._grafo.out_degree(s)== 0:
                self.reddito[s.Product_number] = self._grafo.in_degree(s)
        dizionario_ordinato = dict(sorted(self.reddito.items(), key=lambda x: x[1], reverse=True))
        return dizionario_ordinato, self.ricavo


    def getMethods(self):
        insieme = set()
        metodi = DAO.getAllMetodi()
        for m in metodi:
            insieme.add(m)
        return insieme

    def getCaratteristiche(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

"""
MST Approx Algorithm by CSE6140 fall 2016 Group F
"""

import networkx as nx
import numpy as np
import time
import sys
from heapq import heapify, heappush, heappop
from Queue import Queue

class AlgMA:

    def __init__(self, dsts, cutoffTime):
        self.cutoffTime = cutoffTime
        self.parent = {}
        self.rank = {}
        self.n = dsts.shape[0]

        D = []
        for i in range(self.n):
            for j in range(i + 1, self.n):
                D.append([str(i), str(j), dsts[i, j]])

        self.quality, self.Path, self.trace = self.mst_approx(D)

    def results(self):
        return self.quality, self.Path, self.trace

    def make_set(self, x):
        self.parent[x] = x
        self.rank[x] = 0

    def union(self, x, y):
        root1 = self.find(x)
        root2 = self.find(y)
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2
                if self.rank[root1] == self.rank[root2]:
                    self.rank[root2] += 1

    def find(self, x):
        if self.parent[x] == x:
            return x
        else:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def mst_approx(self, D):

        #creating a graph
        G = nx.Graph()
        G.add_weighted_edges_from(D)

        startTime = time.time()

        #computing MST
        heap = []
        count_orig = 0
        for row in D:
            u, v, w  = row
            heappush(heap, (w, u, v))
            count_orig = count_orig + 1
        for node in G.nodes():
            self.make_set(node)
        MST = set()
        T = nx.Graph()
        sorted_edges = []
        MSTweight = 0
        weight2= 0

        count = 0
        while(count_orig >=1):
            sorted_edges.append(heappop(heap))
            count_orig = count_orig -1
        for edge in sorted_edges:
            w, v1, v2 = edge
            weight2=weight2+w

            if self.find(v1) != self.find(v2):
                self.union(v1, v2)
                MST.add(edge)
                T.add_edge(v1, v2, weight=w)
                MSTweight = MSTweight + w

        bestQuality = sys.maxint / 2
        bestTour = []
        trace = []

        for start in range(self.n):

            #Computing Pre-order traversal path
            Path = list(nx.dfs_preorder_nodes(T, str(start)))
            Last_vertex = Path[0]

            #Computing Hamiltonian Cycle based on pre-order path
            Path.append(Last_vertex)

            #Computing length of tour
            quality = 0
            r = len(Path)
            for i in range(0, r):
                for j in range(i+1, r):
                    a = Path[i]
                    b = Path[j]
                    quality = quality + G[a][b]['weight']
                    break

            if quality < bestQuality:
                bestQuality = quality
                bestTour = Path
                trace.append((time.time() - startTime, bestQuality))
                print time.time() - startTime, bestQuality

        print "Elapsed Time: " + str(time.time() - startTime)

        bestTour = bestTour[:-1]
        for i in range(self.n):
            if bestTour[i] == '0':
                bestTour = bestTour[i:] + bestTour[:i]
                break

        return bestQuality, bestTour, trace

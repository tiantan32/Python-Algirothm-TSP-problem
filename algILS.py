"""
Iterated Local Search Algorithm by CSE6140 fall 2016 Group F
"""

import numpy as np
import random
import time
import sys
import algNN

class AlgILS:

    def __init__(self, dsts, cutoffTime):
        """
        constructor:
        run Nearest Neighbor Algorithm
        in the infinite loop:
            run iterative 2-opt
            check best quality
            run random 4-opt
        """
        self.distances = dsts
        self.cutoffTime = cutoffTime
        self.startTime = time.time()
        self.n = dsts.shape[0]

        # Nearest Neighbor Algorithm
        self.bestQuality, self.bestTour, traceNN = algNN.algNN(dsts, cutoffTime)

        # random initial tour
        # self.bestTour = [i for i in range(self.n)]
        # random.shuffle(self.bestTour)
        # self.bestQuality = self.getQuality(self.bestTour)

        self.curTour = self.bestTour[:]
        self.trace = []

        while True:
            if time.time() - self.startTime > self.cutoffTime:
                print 'Time Out!'
                break
            self.twoOpt()
            quality = self.getQuality(self.curTour)
            if quality < self.bestQuality:
                self.bestQuality = quality
                self.bestTour = self.curTour
                self.trace.append((time.time() - self.startTime, self.bestQuality))
                print time.time() - self.startTime, self.bestQuality
            else:
                self.curTour = self.bestTour[:]
            self.randFourOpt()

        print "Elapsed Time: " + str(time.time() - self.startTime)

        # fw = open('output.log', 'a')
        # fw.write(str(self.bestQuality) + ',')
        # fw.close()

    def getQuality(self, tour):
        """
        get quality from tour
        """
        quality = 0
        for i in range(self.n):
            quality += self.distances[tour[i - 1], tour[i]]
        return quality

    def twoOpt(self):
        """
        run iterative 2-opt
        """
        done = False
        while not done:
            done = True
            for i in range(0, self.n - 2):
                for j in range(i + 1, self.n - 1):
                    before = self.distances[self.curTour[i - 1], self.curTour[i]] + self.distances[self.curTour[j], self.curTour[j + 1]]
                    after = self.distances[self.curTour[i - 1], self.curTour[j]] + self.distances[self.curTour[i], self.curTour[j + 1]]
                    if before > after:
                        done = False
                        self.curTour[i: j + 1] = self.curTour[i: j + 1][::-1]
                        break
                if not done:
                    break

    def randFourOpt(self):
        """
        run random 4-opt
        """
        index = random.sample(range(0, self.n - 1), 4)
        index.sort()
        self.curTour = self.curTour[: index[0]] + self.curTour[index[2]: index[3]] + self.curTour[index[1]: index[2]] + self.curTour[index[0]: index[1]] + self.curTour[index[3]:]

    def results(self):
        """
        return results:
        best quality
        best tour
        trace
        """
        for i in range(self.n):
            if self.bestTour[i] == 0:
                self.bestTour = self.bestTour[i:] + self.bestTour[:i]
                break
        return self.bestQuality, self.bestTour, self.trace

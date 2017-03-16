"""
Branch and Bound Algorithm by CSE6140 fall 2016 Group F
"""

import numpy as np
import time
import sys
import algNN

class AlgBnB:

    def __init__(self, dsts, cutoffTime):
        """
        constructor:
        deal with distances matrix
        calculate initial lower bound
        run recursive function
        """
        distances = dsts.copy()
        self.cutoffTime = cutoffTime
        self.startTime = time.time()
        self.n = distances.shape[0]
        self.bestQuality = sys.maxint / 2
        self.bestTour = {}

        # self.bestQuality, tourNN, traceNN = algNN.algNN(dsts, cutoffTime)
        # for i in range(self.n):
        #     self.bestTour[tourNN[i - 1]] = tourNN[i]

        self.trace = []
        self.timeOut = False
        for i in range(self.n):
            distances[i, i] = sys.maxint / 2
        lowerBound = self.reduceMatrix(distances)
        self.runRecur(distances, [i for i in range(self.n)], [i for i in range(self.n)], lowerBound, {})
        if self.timeOut:
            print 'Time Out!'
        print "Elapsed Time: " + str(time.time() - self.startTime)

    def reduceMatrix(self, mtx):
        """
        reduce distances matrix on rows and columns
        """
        reducedDst = 0
        for i in range(mtx.shape[0]):
            temp = min(mtx[i, :])
            if temp != 0:
                reducedDst += temp
                mtx[i, :] -= np.ones(mtx.shape[0], dtype = int) * temp
        for i in range(mtx.shape[0]):
            temp = min(mtx[:, i])
            if temp != 0:
                reducedDst += temp
                mtx[:, i] -= np.ones(mtx.shape[0], dtype = int) * temp
        return reducedDst

    def existCycle(self, tour, nodeStart):
        """
        check if there exists a cycle in a tour
        """
        temp = nodeStart
        while temp != None:
            temp = tour.get(temp)
            if temp == nodeStart:
                return True
        return False

    def runRecur(self, mtx, idx, idy, lowerBound, tour):
        """
        run recursive functions:
        """

        # cut-off time setup
        if time.time() - self.startTime > self.cutoffTime:
            self.timeOut = True
            return

        # lower bound larger than best quality
        if lowerBound >= self.bestQuality:
            return

        # find new best quality
        if mtx.shape[0] <= 1:
            self.bestQuality = lowerBound
            self.bestTour = tour.copy()
            self.trace.append((time.time() - self.startTime, self.bestQuality))
            print time.time() - self.startTime, self.bestQuality
            return

        # find min from whole matrix
        temp = np.argmin(mtx)
        idxSel = temp / mtx.shape[0]
        idySel = temp % mtx.shape[0]
        minValue = np.amin(mtx)

        # arc included
        tour_new = tour.copy()
        tour_new[idx[idxSel]] = idy[idySel]
        if not self.existCycle(tour_new, idx[idxSel]):
            mtx_new = mtx.copy()
            mtx_new = np.delete(mtx_new, (idxSel), axis = 0)
            mtx_new = np.delete(mtx_new, (idySel), axis = 1)
            temp = self.reduceMatrix(mtx_new)
            lowerBound_new = lowerBound + minValue + temp
            idx_new = idx[:]
            del idx_new[idxSel]
            idy_new = idy[:]
            del idy_new[idySel]
            self.runRecur(mtx_new, idx_new, idy_new, lowerBound_new, tour_new)

        # arc not included
        mtx[idxSel, idySel] = sys.maxint / 2
        temp = min(mtx[idxSel, :])
        if temp != 0:
            lowerBound += temp
            mtx[idxSel, :] -= np.ones(mtx.shape[0], dtype = int) * temp
        temp = min(mtx[:, idySel])
        if temp != 0:
            lowerBound += temp
            mtx[:, idySel] -= np.ones(mtx.shape[0], dtype = int) * temp
        self.runRecur(mtx, idx, idy, lowerBound, tour)

    def results(self):
        """
        return results:
        best quality
        best tour
        trace
        """
        fullList1 = [i for i in range(self.n)]
        keyList = self.bestTour.keys()
        for i in keyList:
            fullList1.remove(i)
        fullList2 = [i for i in range(self.n)]
        valueList = self.bestTour.values()
        for i in valueList:
            fullList2.remove(i)
        self.bestTour[fullList1[0]] = fullList2[0]
        tourList = [0]
        temp = 0
        for i in range(self.n - 1):
            temp = self.bestTour[temp]
            tourList.append(temp)
        return self.bestQuality, tourList, self.trace

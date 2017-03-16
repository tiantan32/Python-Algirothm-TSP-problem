"""
Nearest Neighbor Algorithm by CSE6140 fall 2016 Group F
"""

import time
import sys

def length(tour, D):
    """Calculate the length of a tour according to distance matrix 'D'."""
    z = D[tour[-1]][tour[0]]    # edge from last to first city of the tour
    for i in range(1,len(tour)):
        z += D[tour[i]][tour[i-1]]      # add length of edge from city i-1 to i
    return z

def nearest(last, unvisited, D):
    """Return the index of the node which is closest to 'last'."""
    near = unvisited[0]
    min_dist = D[last][near]
    for i in unvisited[1:]:
        if D[last][i] < min_dist:
            near = i
            min_dist = D[last][near]
    return near

def nearest_neighbor(i, D):
    """Return tour starting from city 'i', using the Nearest Neighbor.

    Uses the Nearest Neighbor heuristic to construct a solution:
    - start visiting city i
    - while there are unvisited cities, follow to the closest one
    - return to city i
    """
    unvisited = D.keys()
    #print 'unvisited',unvisited
    unvisited.remove(i)
    last = i
    tour = [i]
    while unvisited != []:
        next = nearest(last, unvisited, D)
        tour.append(next)
        unvisited.remove(next)
        last = next
    return tour

def algNN(distances, cutoffTime):

    D = {}
    for i in range(distances.shape[0]):
        D[i] = {};
        for j in range(distances.shape[0]):
            D[i][j] = distances[i, j]

    startTime = time.time()
    bestQuality = sys.maxint / 2
    bestTour = []
    trace = []

    for i in D.keys():
        tour = nearest_neighbor(i, D)     # create a greedy tour, visiting city 'i' first
        z = length(tour, D)
        if z < bestQuality:
            bestQuality = z
            bestTour = tour
            trace.append((time.time() - startTime, z))
            print time.time() - startTime, bestQuality

    print "Elapsed Time: " + str(time.time() - startTime)

    for i in range(distances.shape[0]):
        if bestTour[i] == 0:
            bestTour = bestTour[i:] + bestTour[:i]
            break

    return bestQuality, bestTour, trace

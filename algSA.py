"""
Simulated Annealing Algorithm by CSE6140 fall 2016 Group F
"""

import random
import math
import time
import algNN

def neighbor2opt(distances,tspDis,tour):
    # use neighborhood 2 opt method to calculate new tsp value
    n = distances.shape[0]
    i, j = random.sample(range(0, n - 1), 2)
    if i > j:
        i, j = j, i
    newQuality = tspDis + distances[tour[i - 1], tour[j]] + distances[tour[i], tour[(j + 1) % n]] \
    - distances[tour[i - 1], tour[i]] - distances[tour[j], tour[(j + 1) % n]]
    return newQuality, tour[0: i] + tour[i: j + 1][:: -1] + tour[j + 1:]


def algSA(distances, cutoffTime):
    """Minimize the energy of system by simulated annealing

    Parameters: the distances matrix, maximum running time, minimum temperature, maximum temperature, and the number
    of iterations for each temperature.

    Returns: the best location and energy found
    """
    startTime = time.time()
    # Tmax = 1000
    # ratio = 0.999999
    Tmax = 5000
    ratio = 0.999999
    trace = []
    n = distances.shape[0]
    T = Tmax

    bestQuality, bestTour, traceNN = algNN.algNN(distances, cutoffTime)

    allBestQuality = bestQuality

    while True:

        if time.time() - startTime > cutoffTime:
            break

        T = T * ratio

        currentQuality, currentTour = neighbor2opt(distances, bestQuality, bestTour)
        delta = currentQuality - bestQuality

        if delta > 0:
           p = math.exp(-delta / T)
           if random.random() <= p:
              bestQuality = currentQuality
              bestTour = currentTour
        else:
            bestQuality = currentQuality
            bestTour = currentTour

        if bestQuality < allBestQuality:
            allBestQuality = bestQuality
            allBestTour = bestTour
            trace.append((time.time() - startTime, allBestQuality))
            print time.time() - startTime, allBestQuality

    print "Elapsed Time: " + str(time.time() - startTime)

    # fw = open('output.log', 'a')
    # fw.write(str(allBestQuality) + ',')
    # fw.close()

    return bestQuality, bestTour, trace

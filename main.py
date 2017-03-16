"""
Main function by CSE6140 fall 2016 Group F
"""

import argparse
import random
import numpy as np
import os
import math
import time
from algBnB import AlgBnB
import algSA
import algNN
from algMA import AlgMA
from algILS import AlgILS

def main():

    # python main.py -inst DATA/Atlanta.tsp -alg BnB -time 600 -seed 1
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', help = 'file name', type = str, default = 'DATA/Atlanta.tsp')
    parser.add_argument('-alg', help = 'method', type = str, default = 'BnB')
    parser.add_argument('-time', help = 'cut-off time', type = int, default = 600)
    parser.add_argument('-seed', help = 'random seed', type = int, default = 1)
    args = parser.parse_args()

    random.seed(args.seed)

    coordinates, distances = importData(args.inst)

    # Branch-and-Bound
    if args.alg == 'BnB':
        OalgBnB = AlgBnB(distances, args.time)
        quality, tour, trace = OalgBnB.results()
        # quality: quality of best solution found
        # tour: list of ordered locations
        # trace: list of (time, quality)
        # distances: numpy 2d matrix
        # args.time: cut-off time

    # Simulated Annealing
    if args.alg == 'LS1':
        quality, tour, trace = algSA.algSA(distances, args.time)

    # NEAREST NEIGHBOR
    if args.alg == 'Heur':
        quality, tour, trace = algNN.algNN(distances, args.time)

    # MST-APPROX:
    if args.alg == 'MSTApprox':
        OalgMA = AlgMA(distances, args.time)
        quality, tour, trace = OalgMA.results()

    # Iterated Local Search
    if args.alg == 'LS2':
        OalgILS = AlgILS(distances, args.time)
        quality, tour, trace = OalgILS.results()

    # add other algs here

    exportData(args.inst, args.alg, args.time, args.seed, quality, tour, trace, distances)

def importData(fileName):
    with open(fileName, 'r') as fileInput:
        coordinates = []
        for i in range(6):
            curLine = fileInput.readline()
        while (curLine != 'EOF\n'):
            coordinates.append((int(float(curLine.split(' ')[1])), int(float(curLine.split(' ')[2]))))
            curLine = fileInput.readline()
        distances = np.zeros((len(coordinates), len(coordinates)), dtype = int)
        for i in range(len(coordinates)):
            for j in range(i + 1, len(coordinates)):
                distances[i, j] = distances[j, i] = int(round(math.sqrt((coordinates[i][0] - coordinates[j][0]) ** 2 \
                + (coordinates[i][1] - coordinates[j][1]) ** 2)))
    return coordinates, distances

def exportData(inst, alg, time, seed, quality, tour, trace, distances):
    inst = inst.split('/')[-1].split('.')[0]
    if not os.path.exists('OUTPUT'):
        os.makedirs('OUTPUT')
    if alg == 'LS1' or alg == 'LS2':
        fw = open('OUTPUT/' + inst + '_' + alg + '_' + str(time) + '_' + str(seed) + '.sol', 'w')
    else:
        fw = open('OUTPUT/' + inst + '_' + alg + '_' + str(time) + '.sol', 'w')
    fw.write(str(quality) + '\n')
    for i in range(len(tour) - 1):
        fw.write(str(tour[i]) + ' ' + str(tour[i + 1]) + ' ' + str(distances[tour[i], tour[i + 1]]) + '\n')
    fw.write(str(tour[-1]) + ' ' + str(tour[0]) + ' ' + str(distances[tour[-1], tour[0]]) + '\n')
    fw.close()
    if alg == 'LS1' or alg == 'LS2':
        fw = open('OUTPUT/' + inst + '_' + alg + '_' + str(time) + '_' + str(seed) + '.trace', 'w')
    else:
        fw = open('OUTPUT/' + inst + '_' + alg + '_' + str(time) + '.trace', 'w')
    for i in trace:
        fw.write(str(i[0]) + ', ' + str(i[1]) + '\n')
    fw.close()

if __name__ == '__main__':
    main()

import sys, getopt
import os
import networkit as nk
import timeit
import pandas as pd
import numpy as np
import argparse
import csv


parser = argparse.ArgumentParser(prog='evaluation.py')
parser.add_argument('-g', '--graph_name')
parser.add_argument('-p', '--path')
parser.add_argument('-s', '--scenario', choices=['weighted', 'matrix'])
parser.add_argument('-r', '--random_seed', type=int)
parser.add_argument('-o', '--overwrite', action='store_true')
parser.add_argument('-w', '--weights')

args = vars(parser.parse_args())
graph_name = args['graph_name']
csv_path = args['weights']
scenario = args['scenario']
overwrite = args['overwrite']
seed = args['random_seed']
input_path = "../../input/biological/graphs/"
weight_path = "../../input/biological/weights/"
output_path = args['path']
nk.setSeed(seed, False)


def getInitName(i):
    if (i == 0):
        return 'trivial'
    if (i == 1):
        return 'editing'
    if (i == 2):
        return 'random_insert'
    if (i == 3):
        return 'asc_degree_insert'

def executeMover (G, graph_name, init, s, r, p, maxIterations, df, insertEditCost, removeEditCost, weightMatrix):
    if(weightMatrix == None):
        mover = nk.community.QuasiThresholdEditingLocalMover(G, init, max(maxIterations), s, r, p, True, insertEditCost, removeEditCost)
    else:
        mover = nk.community.QuasiThresholdEditingLocalMover(G, init, max(maxIterations), s, r, p, True, 1, 1, weightMatrix)
    a = timeit.default_timer()
    mover.run()
    delta = timeit.default_timer() - a
    edits = mover.getNumberOfEdits()
    editsWeight = mover.getWeightOfEdits()
    usedIterations = mover.getUsedIterations()
    time = delta * 1000
    if(r):
        actualPlateau =  mover.getPlateauSize()
    else:
        actualPlateau = 0
    i = len(df.index)
    editsDevelopement = mover.getRunningInfo()[b'edits']
    editsWeightDevelopement = mover.getRunningInfo()[b'edits_weight']
    for m in maxIterations:
        u = min(m, usedIterations)
        edits = editsDevelopement[u]
        editsWeight = editsWeightDevelopement[u]      
        df.loc[i] = [graph_name, G.numberOfNodes(), getInitName(init), m, s, r, p, insertEditCost, removeEditCost, edits, editsWeight, u, actualPlateau, time]
        i += 1
    return df

def runOnGraph(graph_name, df):
    name = graph_name.split('/')[-1].split('.')[0]
    i = len(df.index)
    graph_path = input_path + graph_name
    if(graph_name.split('/')[0] ==  "facebook100"):
        G = nk.graphio.readMat(input_path + graph_name, key="A")
    if(graph_name.split('.')[-1] == "graph"):
        G = nk.readGraph(graph_path, nk.Format.METIS)
    if(graph_name.split('.')[-1] == "edgelist"):
        G = nk.readGraph(graph_path, nk.Format.SNAP, continuous=False, directed=False)
    if(graph_name.split('.')[-1] == "pairs"):
        G = nk.readGraph(graph_path, nk.Format.SNAP)
    weightMatrix = None
    if(editMatrixUsed):
        with open(weight_path + csv_path, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            # csv_reader = reader(read_obj)
            # Pass reader object to list() to get a list of lists
            weightMatrix = [list(map(int,rec)) for rec in csv.reader(read_obj, delimiter=',')]
    G.indexEdges()
    for insert in insertEditCosts:
        for remove in removeEditCosts:
            for init in initializations:
                for sort in sortPaths:
                    for random in randomness:
                        if(random):
                            for plateau in plateauSize:
                                df = executeMover(G, name, init, sort, random, plateau, maxIterations, df, insert, remove, weightMatrix)
                        else:
                            df = executeMover(G, name, init, sort, random, 0, maxIterations, df, insert, remove, weightMatrix)
    return df

if(scenario == 'weighted'):
    initializations = [1, 2, 3]
    maxIterations = [0, 5, 100]
    sortPaths = [False]
    randomness = [True]
    plateauSize = [5]
    b_queue = False
    insertEditCosts = [1,2]
    removeEditCosts = [1,2]
    weightMatrix = []
    editMatrixUsed = False
if(scenario == 'matrix'):
    initializations = [0, 1, 2, 3]
    maxIterations = [0, 5, 100, 400]
    sortPaths = [True]
    randomness = [True]
    plateauSize = [5,50,100]
    b_queue = False
    insertEditCosts = [1]
    removeEditCosts = [1]
    weightMatrix = []
    editMatrixUsed = True

df = pd.DataFrame(columns  = ['graph',
                              'n',
                              'initialization',
                              'maxIterations',
                              'sortPaths',
                              'randomness',
                              'plateauSize',
                              'insertEditCost',
                              'removeEditCost',
                              'edits',
                              'editsWeight',
                              'usedIterations',
                              'actualPlateau',
                              'time'])


graph_name_simple = graph_name.split('/')[-1].split('.')[0]
output_path += graph_name_simple + '/'

df = runOnGraph(graph_name, df)

if not os.path.exists(output_path):
    os.makedirs(output_path)
df['maxIterations'] = df['maxIterations'].apply(np.int64)
df['plateauSize'] = df['plateauSize'].apply(np.int64)
df['insertEditCost'] = df['insertEditCost'].apply(np.int64)
df['removeEditCost'] = df['removeEditCost'].apply(np.int64)
df['edits'] = df['edits'].apply(np.int64)
df['editsWeight'] = df['editsWeight'].apply(np.int64)
df['usedIterations'] = df['usedIterations'].apply(np.int64)
df['actualPlateau'] = df['actualPlateau'].apply(np.int64)
df['n'] = df['n'].apply(np.int64)
df.to_csv(output_path + graph_name_simple + '_' + scenario + '_' + str(seed) + '.csv', sep=',', encoding='utf-8')

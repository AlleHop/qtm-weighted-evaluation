from networkit import *
import numpy as np
import argparse

parser = argparse.ArgumentParser(prog='forest_stream.py')
parser.add_argument('-p', '--path', help='path of graph', default="../../networkit/input/karate.graph", type=str)
parser.add_argument('-s', '--seed', help='random seed', default=0, type=int)
parser.add_argument('-i', '--init', help='initialisation of algo', default=0, type=int)

args = vars(parser.parse_args())
path = args['path']
seed = args['seed']
init = args['init']
print("seed: ", seed)
print("init: ", init)

setSeed(seed, False)

#G = readGraph("../../networkit/input/karate.graph", Format.METIS)
G = readGraph(path, Format.METIS)
G.indexEdges()
mover = community.QuasiThresholdEditingLocalMover(G, init, 20, True, False, False , 4, True, 2, 2)
mover.run()
D = mover.getDynamicForestGraph()
Q = mover.getQuasiThresholdGraph()
edits = mover.getRunningInfo()[b'edits']
editsCost = mover.getRunningInfo()[b'edits_weight']
Gephi = readGraph(path, Format.METIS)
print("Edits: ", edits)
print("EditCosts: ", editsCost)

for u, v in Q.iterEdges():
    if not G.hasEdge(u,v):
        Gephi.addEdge(u,v)


H = readGraph(path, Format.METIS)
H.indexEdges()
moverSubtree = community.QuasiThresholdEditingLocalMover(H, init, 20, True, False, True, 4, True, 2, 2)
moverSubtree.run()
DSubtree = moverSubtree.getDynamicForestGraph()
QSubtree = moverSubtree.getQuasiThresholdGraph()

editsSubtree = moverSubtree.getRunningInfo()[b'edits']
editsCostSubtree = moverSubtree.getRunningInfo()[b'edits_weight']
print("EditsSubtree: ", editsSubtree)
print("EditCostsSubtree: ", editsCostSubtree)

for u, v in QSubtree.iterEdges():
    if not Gephi.hasEdge(u,v):
        Gephi.addEdge(u,v)

Gephi.indexEdges()

treeEdgesBase =[False for x in range(Gephi.numberOfEdges())]
treeEdgesSubtree =[False for x in range(Gephi.numberOfEdges())]
solEdgesBase =[False for x in range(Gephi.numberOfEdges())]
solEdgesSubtree =[False for x in range(Gephi.numberOfEdges())]
graphEdges =[False for x in range(Gephi.numberOfEdges())]
print("G", G.numberOfEdges())
print("Gephi", Gephi.numberOfEdges())
difference = dynamics.GraphDifference(G, QSubtree)
difference.run()
edgeRemovals = difference.getNumberOfEdgeRemovals()
edgeInsertions = difference.getNumberOfEdgeAdditions()
print("Remove: ", edgeRemovals, " Insertions: ", edgeInsertions)
for u, v in Gephi.iterEdges():
    if G.hasEdge(u ,v):
        graphEdges[Gephi.edgeId(u,v)] = True
    if D.hasEdge(u ,v):
        treeEdgesBase[Gephi.edgeId(u,v)] = True
    if D.hasEdge(v ,u):
        treeEdgesBase[Gephi.edgeId(u,v)] = True
    if DSubtree.hasEdge(u ,v):
        treeEdgesSubtree[Gephi.edgeId(u,v)] = True
    if DSubtree.hasEdge(v ,u):
        treeEdgesSubtree[Gephi.edgeId(u,v)] = True
    if Q.hasEdge(u ,v):
        solEdgesBase[Gephi.edgeId(u,v)] = True
    if Q.hasEdge(v ,u):
        solEdgesBase[Gephi.edgeId(u,v)] = True
    if Q.hasEdge(u ,v):
        solEdgesSubtree[Gephi.edgeId(u,v)] = True
    if QSubtree.hasEdge(v ,u):
        solEdgesSubtree[Gephi.edgeId(u,v)] = True

client = gephi.streaming.GephiStreamingClient(url='http://localhost:8080/workspace0')
client.exportGraph(Gephi)
client.exportEdgeValues(Gephi, treeEdgesBase, "treeEdgesBase")
client.exportEdgeValues(Gephi, treeEdgesSubtree, "treeEdgesSubtree")
client.exportEdgeValues(Gephi, solEdgesBase, "solEdgesBase")
client.exportEdgeValues(Gephi, solEdgesSubtree, "solEdgesSubtree")
client.exportEdgeValues(Gephi, graphEdges, "graphEdges")

clientSubtree = gephi.streaming.GephiStreamingClient(url='http://localhost:8080/workspace1')
clientSubtree.exportGraph(DSubtree)

clientBase = gephi.streaming.GephiStreamingClient(url='http://localhost:8080/workspace2')
clientBase.exportGraph(D)
from networkit import *
import numpy as np
import argparse

parser = argparse.ArgumentParser(prog='forest_stream.py')
parser.add_argument('-n', '--name', help='name of bio graph')
parser.add_argument('-s', '--seed', help='random seed', default=0, type=int)
parser.add_argument('-i', '--init', help='initialisation of algo', default=0, type=int)
parser.add_argument('--subtree', dest='subtree', action='store_true')
parser.add_argument('--no-subtree', dest='subtree', action='store_false')
parser.set_defaults(subtree=True)

args = parser.parse_args()
bioname = args.name
seed = args.seed
init = args.init
subtree = args.subtree
print("seed: ", seed)
print("init: ", init)
print("subtree: ", subtree)

setSeed(seed, False)

#G = readGraph("../../networkit/input/karate.graph", Format.METIS)
G = readGraph("../../input/biological/graphs/" + bioname + ".graph", Format.METIS)
with open("../../input/biological/weights/" + bioname + ".csv", 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    # csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    weightMatrix = [list(map(int,rec)) for rec in csv.reader(read_obj, delimiter=',')]
G.indexEdges()
mover = community.QuasiThresholdEditingLocalMover(G, init, 400, True, True, subtree, 100, True, 1, 1, weightMatrix)
mover.run()
D = mover.getDynamicForestGraph()
Q = mover.getQuasiThresholdGraph()
edits = mover.getRunningInfo()[b'edits']
editsCost = mover.getRunningInfo()[b'edits_weight']
Gephi = readGraph("../../input/biological/graphs/" + bioname + ".graph", Format.METIS)
print("Edits: ", edits)
print("EditCosts: ", editsCost)

for u, v in Q.iterEdges():
    if not G.hasEdge(u,v):
        Gephi.addEdge(u,v)


#G = readGraph("../../networkit/input/karate.graph", Format.METIS)
H = readGraph("../../input/optimization/graphs/" + bioname + "-opt.graph", Format.METIS)
with open("../../input/optimization/weights/" + bioname + "-opt.csv", 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    # csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    weightMatrix = [list(map(int,rec)) for rec in csv.reader(read_obj, delimiter=',')]
H.indexEdges()
moverOpt = community.QuasiThresholdEditingLocalMover(H, init, 400, True, True, subtree, 100, True, 1, 1, weightMatrix)
moverOpt.run()
DOpt = moverOpt.getDynamicForestGraph()
QOpt = moverOpt.getQuasiThresholdGraph()

editsOpt = moverOpt.getRunningInfo()[b'edits']
editsCostOpt = moverOpt.getRunningInfo()[b'edits_weight']
print("EditsOpt: ", editsOpt)
print("EditCostsOpt: ", editsCostOpt)

for u, v in QOpt.iterEdges():
    if not Gephi.hasEdge(u,v):
        Gephi.addEdge(u,v)

Gephi.indexEdges()

treeEdgesQTM =[False for x in range(Gephi.numberOfEdges())]
treeEdgesOpt =[False for x in range(Gephi.numberOfEdges())]
solEdgesQTM =[False for x in range(Gephi.numberOfEdges())]
solEdgesOpt =[False for x in range(Gephi.numberOfEdges())]
graphEdges =[False for x in range(Gephi.numberOfEdges())]
print("G", G.numberOfEdges())
print("Gephi", Gephi.numberOfEdges())
for u, v in Gephi.iterEdges():
    if G.hasEdge(u ,v):
        graphEdges[Gephi.edgeId(u,v)] = True
    if D.hasEdge(u ,v):
        treeEdgesQTM[Gephi.edgeId(u,v)] = True
    if D.hasEdge(v ,u):
        treeEdgesQTM[Gephi.edgeId(u,v)] = True
    if DOpt.hasEdge(u ,v):
        treeEdgesOpt[Gephi.edgeId(u,v)] = True
    if DOpt.hasEdge(v ,u):
        treeEdgesOpt[Gephi.edgeId(u,v)] = True
    if Q.hasEdge(u ,v):
        solEdgesQTM[Gephi.edgeId(u,v)] = True
    if Q.hasEdge(v ,u):
        solEdgesQTM[Gephi.edgeId(u,v)] = True
    if QOpt.hasEdge(u ,v):
        solEdgesOpt[Gephi.edgeId(u,v)] = True
    if QOpt.hasEdge(v ,u):
        solEdgesOpt[Gephi.edgeId(u,v)] = True

client = gephi.streaming.GephiStreamingClient(url='http://localhost:8080/workspace0')
client.exportGraph(Gephi)
client.exportEdgeValues(Gephi, treeEdgesQTM, "treeEdgesQTM")
client.exportEdgeValues(Gephi, treeEdgesOpt, "treeEdgesOpt")
client.exportEdgeValues(Gephi, solEdgesQTM, "solEdgesQTM")
client.exportEdgeValues(Gephi, solEdgesOpt, "solEdgesOpt")
client.exportEdgeValues(Gephi, graphEdges, "graphEdges")

clientTree = gephi.streaming.GephiStreamingClient(url='http://localhost:8080/workspace1')
clientTree.exportGraph(DOpt)

clientQTM = gephi.streaming.GephiStreamingClient(url='http://localhost:8080/workspace2')
clientQTM.exportGraph(D)
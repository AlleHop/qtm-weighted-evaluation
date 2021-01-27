from networkit import *
import numpy as np

setSeed(0, False)

#G = readGraph("../../networkit/input/karate.graph", Format.METIS)
G = readGraph("../../input/biological/graphs/bio-nr-2666-size-20.graph", Format.METIS)
with open("../../input/biological/weights/bio-nr-2666-size-20.csv", 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    # csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    weightMatrix = [list(map(int,rec)) for rec in csv.reader(read_obj, delimiter=',')]
G.indexEdges()
mover = community.QuasiThresholdEditingLocalMover(G, 0, 400, True, True, 100, True, 1, 1, weightMatrix)
mover.run()
D = mover.getDynamicForestGraph()
Q = mover.getQuasiThresholdGraph()
edits = mover.getRunningInfo()[b'edits']
editsCost = mover.getRunningInfo()[b'edits_weight']
Gephi = readGraph("../../input/biological/graphs/bio-nr-2666-size-20.graph", Format.METIS)
print("Edits: ", edits)
print("EditCosts: ", editsCost)

for u, v in Q.iterEdges():
    if not G.hasEdge(u,v):
        Gephi.addEdge(u,v)
Gephi.indexEdges()

#G = readGraph("../../networkit/input/karate.graph", Format.METIS)
H = readGraph("../../input/optimization/graphs/bio-nr-2666-size-20-opt.graph", Format.METIS)
with open("../../input/optimization/weights/bio-nr-2666-size-20-opt.csv", 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    # csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    weightMatrix = [list(map(int,rec)) for rec in csv.reader(read_obj, delimiter=',')]
H.indexEdges()
moverOpt = community.QuasiThresholdEditingLocalMover(H, 0, 400, True, True, 100, True, 1, 1, weightMatrix)
moverOpt.run()
DOpt = moverOpt.getDynamicForestGraph()
QOpt = moverOpt.getQuasiThresholdGraph()

treeEdgesQTM =[False for x in range(Gephi.numberOfEdges())]
treeEdgesOpt =[False for x in range(Gephi.numberOfEdges())]
solEdgesQTM =[False for x in range(Gephi.numberOfEdges())]
solEdgesOpt =[False for x in range(Gephi.numberOfEdges())]
graphEdges =[False for x in range(Gephi.numberOfEdges())]
print("G", G.numberOfEdges())
print("Gephi", Gephi.numberOfEdges())
for u, v in Gephi.iterEdges():
    if G.hasEdge(u ,v):
        print("Graph Id:",Gephi.edgeId(u,v), "Nodes", u ,",",v )
        graphEdges[Gephi.edgeId(u,v)] = True
    if D.hasEdge(u ,v):
        treeEdgesQTM[Gephi.edgeId(u,v)] = True
    if D.hasEdge(v ,u):
        treeEdgesQTM[G.edgeId(u,v)] = True
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
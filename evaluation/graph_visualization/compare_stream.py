from networkit import *

setSeed(0, False)

#G = readGraph("../../networkit/input/karate.graph", Format.METIS)
G = readGraph("../../input/biological/graphs/bio-nr-2666-size-20.graph", Format.METIS)
with open("../../input/biological/weights/bio-nr-2666-size-20.csv", 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    # csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    weightMatrix = [list(map(int,rec)) for rec in csv.reader(read_obj, delimiter=',')]
G.indexEdges()
mover = community.QuasiThresholdEditingLocalMover(G, 0, 400, True, True, False, 100, True, 1, 1, weightMatrix)
mover.run()
Q = mover.getQuasiThresholdGraph()
client = gephi.streaming.GephiStreamingClient(url='http://localhost:8080/workspace0')
client.exportGraph(Q)
edits = mover.getRunningInfo()[b'edits']
editsCost = mover.getRunningInfo()[b'edits_weight']

print("Edits: ", edits)
print("EditCosts: ", editsCost)

communities = community.detectCommunities(Q)
client.exportNodeValues(G, communities, "community")

#G = readGraph("../../networkit/input/karate.graph", Format.METIS)
H = readGraph("../../input/optimization/graphs/bio-nr-2666-size-20-opt.graph", Format.METIS)
with open("../../input/optimization/weights/bio-nr-2666-size-20-opt.csv", 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    # csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    weightMatrix = [list(map(int,rec)) for rec in csv.reader(read_obj, delimiter=',')]
H.indexEdges()
mover2 = community.QuasiThresholdEditingLocalMover(H, 0, 400, True, True, False, 100, True, 1, 1, weightMatrix)
mover2.run()
QOpt = mover2.getQuasiThresholdGraph()
clientOpt = gephi.streaming.GephiStreamingClient(url='http://localhost:8080/workspace1')
clientOpt.exportGraph(H)
edits = mover2.getRunningInfo()[b'edits']
editsCost = mover2.getRunningInfo()[b'edits_weight']

print("EditsOpt: ", edits)
print("EditCostsOpt: ", editsCost)

communities = community.detectCommunities(H)
clientOpt.exportNodeValues(H, communities, "community")

clientStart = gephi.streaming.GephiStreamingClient(url='http://localhost:8080/workspace2')
clientStart.exportGraph(G)
communities = community.detectCommunities(G)
clientStart.exportNodeValues(G, communities, "community")
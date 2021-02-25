from networkit import *


#G = readGraph("../../networkit/input/karate.graph", Format.METIS)
G = readGraph("../../input/biological/graphs/bio-nr-233-size-80.graph", Format.METIS)
with open("../../input/biological/weights/bio-nr-233-size-80.csv", 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    # csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    weightMatrix = [list(map(int,rec)) for rec in csv.reader(read_obj, delimiter=',')]

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
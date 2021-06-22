from networkit import *
import argparse
import scipy
import numpy as np

parser = argparse.ArgumentParser(prog='gephi_stream.py')
parser.add_argument('-n', '--name', help='name of bio graph')
parser.add_argument('-s', '--seed', help='random seed', default=0, type=int)
parser.add_argument('-in', '--init', help='initialisation of algo', default=0, type=int)
parser.add_argument('-i', '--insert', default=1, type=int)
parser.add_argument('-r', '--remove', default=1, type=int)
parser.add_argument('--subtree', dest='subtree', action='store_true')
parser.add_argument('--no-subtree', dest='subtree', action='store_false')
parser.set_defaults(subtree=True)
parser.add_argument('--sort', dest='sort', action='store_true')
parser.add_argument('--no-sort', dest='sort', action='store_false')
parser.set_defaults(sort=False)


args = vars(parser.parse_args())
facebookname = args['name']
seed = args['seed']
init = args['init']
insert = args['insert']
remove = args['remove']
subtree = args['subtree']
sort = args['sort']
print("seed: ", seed)
print("init: ", init)

#G = readGraph("../../input/facebook/graphs/" + bioname + ".graph", Format.METIS)
G = graphio.readMat("../../input/facebook/graphs/" + facebookname + ".mat", key="A")

G.indexEdges()
mover = community.QuasiThresholdEditingLocalMover(G, init, 400, True, True, subtree , sort , 100, True, insert, remove)
mover.run()
D = mover.getDynamicForestGraph()
Q = mover.getQuasiThresholdGraph()
edits = mover.getRunningInfo()[b'edits']
editsCost = mover.getRunningInfo()[b'edit_costs']
print("Edits: ", edits)
print("EditCosts: ", editsCost)


difference = dynamics.GraphDifference(G ,Q)
difference.run()
edgeRemovals = difference.getNumberOfEdgeRemovals()
edgeInsertions = difference.getNumberOfEdgeAdditions()
print("Remove: ", edgeRemovals, " Insertions: ", edgeInsertions)

fb_attr = "../../input/facebook/graphs/Caltech36.mat"
matlabObject = scipy.io.loadmat(fb_attr)
array = np.array(matlabObject["local_info"])
array = array[:,4]
d = array.tolist()
attribute_dict = {
    "student_fac" : 0,
    "gender" : 1,
    "major_index" : 2,
    "second_major" : 3,
    "dorm" : 4,
    "year" : 5,
    "high_school" : 6,
}

for attribute in ["dorm"]:
    if attribute not in attribute_dict:
        raise Exception("Attribute {0} not found".format(attribute))

    value_dict = {}
    col = attribute_dict[attribute]

    for u, a in enumerate(matlabObject['local_info'][:,col]):
        value_dict[a] = u

client = gephi.streaming.GephiStreamingClient(url='http://localhost:8080/workspace1')
client.exportGraph(Q)

communities = community.detectCommunities(Q)
client.exportNodeValues(Q, communities, "community")
client.exportNodeValues(Q, d, "dorm")
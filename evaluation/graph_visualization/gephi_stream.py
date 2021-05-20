from networkit import *
import argparse
import scipy
import numpy as np

parser = argparse.ArgumentParser(prog='forest_stream.py')
parser.add_argument('-p', '--path', help='path to facebook graph')

fb_attr = "../../input/facebook/graphs/Caltech36.mat"
matlabObject = scipy.io.loadmat(fb_attr)
array = np.array(matlabObject["local_info"])
array = array[:,4]
d = array.tolist()
print(d)
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

args = parser.parse_args()
facebookname = args.path
#G = readGraph("../../networkit/input/karate.graph", Format.METIS)
G = readGraph(facebookname, Format.METIS)
client = gephi.streaming.GephiStreamingClient(url='http://localhost:8080/workspace1')
client.exportGraph(G)

communities = community.detectCommunities(G)
print(communities)
client.exportNodeValues(G, communities, "community")
client.exportNodeValues(G, d, "dorm")
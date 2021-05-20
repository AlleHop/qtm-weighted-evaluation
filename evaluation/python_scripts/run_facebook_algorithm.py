import networkit  as nk
import argparse

parser = argparse.ArgumentParser(prog='forest_stream.py')
parser.add_argument('-n', '--name', help='name of facebook graph')
parser.add_argument('-s', '--seed', help='random seed', default=0, type=int)
parser.add_argument('--insert', help='insert cost', default=1, type=int)
parser.add_argument('--remove', help='remove cost', default=1, type=int)
parser.add_argument('-i', '--init', help='initialisation of algo', default=0, type=int)
parser.add_argument('-iter', '--iterations', help='number of runs', default=400, type=int)
parser.add_argument('--subtree', dest='subtree', action='store_true')
parser.add_argument('--no-subtree', dest='subtree', action='store_false')
parser.set_defaults(subtree=True)
parser.add_argument('--sort', dest='sort', action='store_true')
parser.add_argument('--no-sort', dest='sort', action='store_false')
parser.set_defaults(sort=True)

args = parser.parse_args()
facebookname = args.name
seed = args.seed
remove = args.remove
insert= args.insert
init = args.init
iterations = args.iterations
subtree = args.subtree
sort = args.sort
print("seed: ", seed)
print("init: ", init)
print("iterations: ", iterations)
print("subtree: ", subtree)
print("sort: ", sort)

nk.setSeed(seed, False)

G = nk.graphio.readMat("../../input/facebook/graphs/" + facebookname + ".mat", key="A")
G.indexEdges()
mover = nk.community.QuasiThresholdEditingLocalMover(G, init, iterations, True, True, subtree, sort, 100, True, insert, remove)
mover.run()
D = mover.getDynamicForestGraph()
Q = mover.getQuasiThresholdGraph()
nk.graphio.writeGraph(Q, "../output/facebook/graphs/" + facebookname + "-seed-"+ str(seed) + "-init-"+ str(init) + "-subtree-"+ str(subtree) + "-sort-"+ str(sort) + ".graph",nk.graphio.Format.METIS)
edits = mover.getNumberOfEdits()
editCosts = mover.getCostOfEdits()
print("Edits: ", edits)
print("EditCosts: ", editCosts)
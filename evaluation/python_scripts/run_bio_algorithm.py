import networkit  as nk
import argparse

parser = argparse.ArgumentParser(prog='forest_stream.py')
parser.add_argument('-n', '--name', help='name of bio graph')
parser.add_argument('-s', '--seed', help='random seed', default=0, type=int)
parser.add_argument('-i', '--init', help='initialisation of algo', default=0, type=int)
parser.add_argument('-iter', '--iterations', help='number of runs', default=400, type=int)
parser.add_argument('--subtree', dest='subtree', action='store_true')
parser.add_argument('--no-subtree', dest='subtree', action='store_false')
parser.set_defaults(subtree=True)

args = parser.parse_args()
bioname = args.name
seed = args.seed
init = args.init
iterations = args.iterations
subtree = args.subtree
print("seed: ", seed)
print("init: ", init)
print("iterations: ", iterations)
print("subtree: ", subtree)

nk.setSeed(seed, False)

#G = readGraph("../../networkit/input/karate.graph", Format.METIS)
G = nk.readGraph("../../input/biological/graphs/" + bioname + ".graph", Format.METIS)
with open("../../input/biological/weights/" + bioname + ".csv", 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    # csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    weightMatrix = [list(map(int,rec)) for rec in csv.reader(read_obj, delimiter=',')]
G.indexEdges()
mover = nk.community.QuasiThresholdEditingLocalMover(G, init, iterations, True, True, subtree, False, 100, True, 1, 1, weightMatrix)
mover.run()
D = mover.getDynamicForestGraph()
Q = mover.getQuasiThresholdGraph()
edits = mover.getNumberOfEdits()
editCosts = mover.getCostOfEdits()
print("Edits: ", edits)
print("EditCosts: ", editCosts)
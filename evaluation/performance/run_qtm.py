#!/usr/bin/env python3

import glob
import os
import sys
import timeit
import networkit as nk

nk.setNumberOfThreads(1)

# Facebook graphs
facebook_paths = sorted(glob.glob(
    os.path.expanduser("/amd.home/algoDaten/haman/graphs/facebook100/[A-Z]*.mat")))
print(facebook_paths)
assert len(facebook_paths) == 100

# Bio graphs
bio_paths = sorted(glob.glob(
    os.path.expanduser("~/graphs/biological/metis_graphs/*.cm")))
assert len(bio_paths) == 3964

# Generated graphs
generated_paths = sorted(glob.glob(
    os.path.expanduser("~/Dokumente/Paper/2015-Quasi-Threshold-Editing/data/*.metis.graph")))
assert len(generated_paths) == 24

# Generated graphs (for final experiments)
generated_paths = sorted(glob.glob(
    os.path.expanduser("~/Dokumente/Paper/2015-Quasi-Threshold-Editing/data/*.metis.graph")))

all_configs = [
    "QTM-no-init-no-sort-no-random",
    "QTM-edit-init-no-sort-no-random",
    "QTM-asc-min-init-sort-no-random",
    "QTM-asc-min-init-sort-random",
    "QTM-edit-init-sort-random",
    "QTM-rand-min-init-sort-random",
    "QTM-rand-min-init-sort-no-random",
    "QTM-desc-min-init-sort-no-random",
    "QTM-desc-min-init-sort-random",
    "QTM-edit-init-no-sort-random",
    "QTM-edit-init-sort-no-random",
    "QTM-no-init-sort-random",
    "QTM-no-init-sort-no-random",
    "QTM-no-init-no-sort-random"
    ]

final_configs = [
    "QTM-no-init-no-sort-no-random",
    "QTM-edit-init-no-sort-no-random",
    "QTM-rand-min-init-sort-random",
    "QTM-no-init-sort-random",
    "QTM-edit-init-sort-random"
]

def randomize_graph(graph):
    idmap = nk.graphtools.getRandomContinuousNodeIds(graph)
    gr = nk.graphtools.getCompactedGraph(graph, idmap)
    gr.sortEdges()
    gr.indexEdges()
    return gr

def init_qtm(graph, conf, iterations=400):
    """
    Initialize a QuasiThresholdEditingLocalMover for the given configuration.
    """
    init = nk.community.QuasiThresholdEditingLocalMover.Trivial
    if "edit-init" in conf:
        init = nk.community.QuasiThresholdEditingLocalMover.Editing
    elif "asc-min-init" in conf:
        init = nk.community.QuasiThresholdEditingLocalMover.AscDegreeInsert
    elif "desc-min-init" in conf:
        init = nk.community.QuasiThresholdEditingLocalMover.DescDegreeInsert
    elif "rand-min-init" in conf:
        init = nk.community.QuasiThresholdEditingLocalMover.RandomInsert
    else:
        assert 'no-init' in conf

    sort_paths = "no-sort" not in conf
    randomness = "no-random" not in conf

    return nk.community.QuasiThresholdEditingLocalMover(graph, init, iterations,
                                                        sort_paths,
                                                        randomness, min(iterations, 100))


# Create table with:
# Graph Algorithm Seed Iteration Total_Time Edits Time Nodes_Moved Cache_Misses Cache_References Cycles Instructions

def run_experiment(dataset, gp, conf, graph_format, num_samples=10, file=sys.stdout, iterations=400):
    name, ext = os.path.splitext(os.path.basename(gp))
    if ext == ".mat":
        graph = nk.graphio.readMat(gp, 'A')
    else:
        graph = nk.readGraph(gp, graph_format)

    print(name, hash(tuple([name, 0])) & 0xffffffffffffffff, conf)

    for i in range(num_samples):
        nk.setSeed(hash(tuple([name, i])) & 0xffffffffffffffff, False)
        randomized_graph = randomize_graph(graph)
        qtm = init_qtm(randomized_graph, conf, iterations=iterations)
        total_time = timeit.timeit(qtm.run, number=1)
        stats = qtm.getRunningInfo()

        print_line(dataset, name, conf, i, -1, "Time [s]", total_time, file=file)
        print_line(dataset, name, conf, i, -1, "Edits", qtm.getNumberOfEdits(), file=file)
        print_line(dataset, name, conf, i, -1, "n", randomized_graph.numberOfNodes(), file=file)
        print_line(dataset, name, conf, i, -1, "m", randomized_graph.numberOfEdges(), file=file)
        print_line(dataset, name, conf, i, -1, "Iterations", qtm.getUsedIterations(), file=file)
        for stat_name, stat_values in stats.items():
            utf8_stat_name = stat_name.decode("utf-8")
            for iteration, stat in enumerate(stat_values):
                print_line(dataset, name, conf, i, iteration, utf8_stat_name, stat, file=file)

        del qtm
        del randomized_graph


def print_line(dataset, name, conf, sample, iteration, stat_name, stat, file=sys.stdout):
    if isinstance(stat, float):
        print('"{}","{}","{}",{},{},"{}",{:.6}'.format(dataset, name, conf, sample, iteration, stat_name, stat), file=file)
    else:
        print('"{}","{}","{}",{},{},"{}",{}'.format(dataset, name, conf, sample, iteration, stat_name, stat), file=file)


def print_header(file=sys.stdout):
    print_line("Dataset", "Graph", "Algorithm", "Sample", "Iteration", "Name", "Value", file=file)


# Bio-Graphs
BIO_OUTPUT = "bio_results-all.csv"
if os.path.exists(BIO_OUTPUT):
    print("File {} exists, skipping".format(BIO_OUTPUT))
else:
    with open(BIO_OUTPUT, "w") as bio_file:
        print_header(bio_file)
        for bio_path in bio_paths:
            for my_conf in all_configs:
                run_experiment("bio", bio_path, my_conf, nk.Format.METIS, file=bio_file)


FB_OUTPUT = "fb_results-all.csv"
if os.path.exists(FB_OUTPUT):
    print("File {} exists, skipping".format(FB_OUTPUT))
else:
    with open(FB_OUTPUT, "w") as fb_file:
        print_header(fb_file)

        for fb_path in facebook_paths:
            for my_conf in all_configs:
                run_experiment("fb", fb_path, my_conf, nk.Format.MAT, file=fb_file)


GENERATED_OUTPUT = "generated_results.csv"
if os.path.exists(GENERATED_OUTPUT):
    print("File {} exists, skipping".format(GENERATED_OUTPUT))
else:
    with open(GENERATED_OUTPUT, "w") as generated_file:
        print_header(generated_file)

        for gen_path in generated_paths:
            for my_conf in final_configs:
                run_experiment("generated", gen_path, my_conf, nk.Format.METIS, file=generated_file, iterations=50)


LARGE_OUTPUT = "large_results.csv"
if os.path.exists(LARGE_OUTPUT):
    print("File {} exists, skipping".format(LARGE_OUTPUT))
else:
    with open(LARGE_OUTPUT, "w") as large_file:
        print_header(large_file)

        names = ["cnr-2000", "eu-2005", "in-2004", "com-youtube", "com-dblp", "com-amazon", "com-lj", "uk-2002", "com-orkut"]
        for name in names:
            print(name)
            sys.stdout.flush()

            if name[0:3] in ["ca-", "com"]:
                path = "/amd.home/algoDaten/graphs/parco/Static/SNAP/{}.ungraph.txt".format(name)
                graph_format = nk.Format.SNAP
            else:
                path = "/amd.home/algoDaten/graphs/parco/Static/DIMACS/Clustering/{}.metis.graph".format(name)
                if not os.path.isfile(path):
                    path = "/amd.home/algoDaten/graphs/parco/Static/DIMACS/Large/{}.metis.graph".format(name)

                graph_format = nk.Format.METIS

            for my_conf in final_configs:
                run_experiment("large", path, my_conf, graph_format, file=large_file, iterations=50)


#!/usr/bin/env python3

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert metis .graph files to csv weight files')
    parser.add_argument('--remove', help='remove edit cost', default=1, type=int)
    parser.add_argument('--insert', help='insert edit cost', default=1, type=int)
    parser.add_argument('input', help='The input file')
    parser.add_argument('output', help='The output file')

    args = parser.parse_args()

    n = m = 0
    int_weight = 0

    with open(args.input, 'r') as input_file:
        for ln, line in enumerate(input_file):
            if ln == 0:
                parameters = line.split(' ')
                n = int(parameters[0])
                edges = int(parameters[1])
                neighbors = [[0 for i in range(n)] for i in range(n)]
            elif line.rstrip():
                line.strip()
                all_neighbors = line.split(' ')
                all_neighbors.pop()
                assert(len(all_neighbors) <= n)
                m = 0
                for i, v in enumerate(map(int, all_neighbors)):
                    while m <= v-1:
                        neighbors[ln-1][m] = -args.insert
                        if m == v-1:
                            neighbors[ln-1][m] = args.remove
                        m += 1
                while m <= n-1:
                    neighbors[ln-1][m] = -args.insert
                    m += 1
    with open(args.output, 'w') as output_file:
        #print("{} {} 0".format(n, m), file=output_file)
        for neigh in neighbors:
            print("{}".format(",".join(map(str, neigh))), file=output_file)

#!/usr/bin/env python3

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert protein .cm files to metis graph files')
    parser.add_argument('--threshold', help='The threshold', default=0, type=float)
    parser.add_argument('input', help='The input file')
    parser.add_argument('output', help='The output file')

    args = parser.parse_args()

    n = m = 0
    neighbors = []
    with open(args.input, 'r') as input_file:
        for ln, line in enumerate(input_file):
            n += 1
            all_neighbors = line.split(',')
            neighbor_of_node = []
            #assert(len(all_neighbors) == expected_neighbors)
            for i, weight in enumerate(map(float, all_neighbors)):
                if weight > args.threshold:
                   neighbor_of_node.append(i + 1)
                   m += 1
            neighbors.append(neighbor_of_node)
    m = int(m/2)
    with open(args.output, 'w') as output_file:
        print("{} {} 0".format(n, m), file=output_file)
        for neigh in neighbors:
            print("{}".format(" ".join(map(str, neigh))), file=output_file)

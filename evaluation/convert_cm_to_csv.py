#!/usr/bin/env python3

import argparse
import math

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert protein .cm files to csv weight files')
    parser.add_argument('--threshold', help='The threshold', default=0, type=float)
    parser.add_argument('--multiplier', help='The multiplier', default=100, type=int)
    parser.add_argument('input', help='The input file')
    parser.add_argument('output', help='The output file')

    args = parser.parse_args()

    n = m = 0
    int_weight = 0

    with open(args.input, 'r') as input_file:
        for ln, line in enumerate(input_file):
            if ln == 0:
                n = int(line)
                neighbors = [[0 for i in range(n)] for i in range(n)]
            elif ln <= n:
                continue
            elif line.rstrip():
                u = ln - n
                
                expected_neighbors = n - u

                all_neighbors = line.split('\t')

                assert(len(all_neighbors) == expected_neighbors)

                for i, weight in enumerate(map(float, all_neighbors)):
                    v = u + i + 1
                    int_weight = math.ceil(abs(weight * args.multiplier))
                    if weight >= args.threshold:
                        neighbors[u-1][v-1] = int_weight
                        neighbors[v-1][u-1] = int_weight
                        m += 1
                    else :
                        neighbors[u-1][v-1] = (-1) * int_weight
                        neighbors[v-1][u-1] = (-1) * int_weight
                        m += 1

    with open(args.output, 'w') as output_file:
        #print("{} {} 0".format(n, m), file=output_file)
        for neigh in neighbors:
            print("{}".format(",".join(map(str, neigh))), file=output_file)

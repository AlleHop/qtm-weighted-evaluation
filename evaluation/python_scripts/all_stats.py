import os
import pandas as pd
import argparse
import numpy as np

def print_percentile_improvement(df, base_algo, comparison_algo, min_time):
    solved_time_calls_base_min = df[(df['time', base_algo] >= min_time) & df['time', comparison_algo].notna()]
    print("Of {} instances where {} needed at least {} seconds, {} was faster".format(len(solved_time_calls_base_min), base_algo, min_time, comparison_algo))
    for measure in ['edits', 'time']:
        print(measure)
        solved_measure_base_min = solved_time_calls_base_min[measure].copy()
        assert(len(solved_measure_base_min) == len(solved_time_calls_base_min))

        assert(not solved_measure_base_min[base_algo].hasnans)
        assert(not solved_measure_base_min[comparison_algo].hasnans)
        # Restrict to graphs solved by both algorithms
        #if measure == 'Calls' and solved_measure_base_min[comparison_algo].hasnans:
        #    solved_measure_base_min = solved_measure_base_min[solved_measure_base_min[comparison_algo].notna() & solved_measure_base_min[base_algo].notna()]
        #    print("Restricting to {} instances solved by both algorithms".format(len(solved_measure_base_min)))
        #else:
        #    solved_measure_base_min[comparison_algo].fillna(np.inf, inplace=True)
        #    solved_measure_base_min[base_algo].fillna(np.inf, inplace=True)

        speedup = (solved_measure_base_min[base_algo] / solved_measure_base_min[comparison_algo]).to_numpy()
        assert(not np.isnan(speedup).any())
        percentiles = np.array([0, 0.1, 1, 5, 10, 25, 50, 75, 90, 95, 99, 99.9, 100])
        speedup_percentiles = np.percentile(speedup, percentiles)
        assert(not np.isnan(speedup_percentiles).any())
        for p, s in zip(percentiles, speedup_percentiles):
            print("  on {:.1f}% of the instances {:.2f} faster".format(100-p, s))

        #for speedup in [1, 1.1, 1.5, 2, 5, 8, 10, 20, 50, 80, 100, 200, 500, 800, 1000]:
        #    num_faster = sum(solved_measure_base_min[comparison_algo] * speedup <= solved_measure_base_min[base_algo])
        #    fraction_faster = num_faster / len(solved_measure_base_min)
        #    print(" {} times on {} ({:.2%}) instances ".format(speedup, num_faster, fraction_faster))


parser = argparse.ArgumentParser(prog='path')
parser.add_argument('-p', '--path')

args = vars(parser.parse_args())
path = args['path']

result = []
df = pd.read_csv(path)

df_unstacked = df.unstack()
for base_algo, comparison_algo in [
            ('QTM-nonuniform-edit-init-subtree', 'QTM-nonuniform-edit-init-no-subtree'),
            ('ILP-S', 'ILP-S-R'),
            ('ILP-S-R', 'ILP-S-R-C4')
            ]:
    print_percentile_improvement(df, base_algo, comparison_algo, 0)





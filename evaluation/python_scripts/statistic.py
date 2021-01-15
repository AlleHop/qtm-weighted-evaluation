import sys, getopt
import os
import networkit as nk
import timeit
import pandas as pd
import numpy as np
import argparse


parser = argparse.ArgumentParser(prog='statistic.py')
parser.add_argument('-path', '--path')

args = vars(parser.parse_args())
path = args['path']

parent_path = '/'.join(path.split('/')[:-2]) + '/'
output_path = path + "statistic/"
result = []
for file in os.listdir(path + "sorted/"):
    if file.endswith("_compare.csv"):
        output_d = {'graph_set': ['bio']}
        output_df = pd.DataFrame(data=output_d)
        df = pd.read_csv(path + "sorted/"+ file)
        sum_exact_list = []
        sum_noexact_list = []
        sum_good_list = []
        sum_bad_list = []
        sum_exact = len(df[(df['ratio']==1.0)])
        sum_exact_list.append(sum_exact)
        sum_noexact = len(df[(df['ratio']==-1.0)])
        sum_noexact_list.append(sum_noexact)
        sum_good = len(df[(df['ratio']>1.0) & (df['ratio']<=1.5)])
        sum_good_list.append(sum_good)
        sum_bad = len(df[(df['ratio']>1.5)])
        sum_bad_list.append(sum_bad)
        output_df.insert(1,'exact_solved', sum_exact_list)
        output_df.insert(2,'no_exact_solution', sum_noexact_list)
        output_df.insert(3,'solved<1.5', sum_good_list)
        output_df.insert(3,'solved>1.5', sum_bad_list)
        print(output_df)
        #del output_df['Unnamed: 0']
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_df.to_csv(output_path + file.strip("_"), sep=',', encoding='utf-8')


    

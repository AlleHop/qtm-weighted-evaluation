import sys, getopt
import os
import networkit as nk
import timeit
import pandas as pd
import numpy as np
import argparse


parser = argparse.ArgumentParser(prog='minimum_editcost.py')
parser.add_argument('-p', '--path')

args = vars(parser.parse_args())
path = args['path']

parent_path = '/'.join(path.split('/')[:-2]) + '/'
for root, dirs, f in os.walk(path):
    #dirs = dirs[1:]
    result = []
    for dir in dirs:
        filenames = []
        for file in os.listdir(path + '/' + dir):
            filenames.append(file)
        output_name = '_'.join(filenames[0].split('_')[1:-1]) + '_minimum.csv'
        df = pd.read_csv(path + '/' + dir +'/'+ filenames[0])
        dfs = np.split(df, [10], axis=1)
        input_df = dfs[0]
        for i in range(0, len(filenames)):
            df = np.split(pd.read_csv(path + '/' + dir +'/'+ filenames[i]), [10], axis=1)[1]
            minimum_list = df.apply(pd.to_numeric).idxmin(axis=0)       
            output_df = df.iloc[[minimum_list[0]]]
        output_df = input_df.join(output_df, how = 'right')
        del output_df['Unnamed: 0']
        result.append(output_df)
    result_df = result[0]
    for i in range(1, len(result)):
        result_df = pd.concat((result_df, result[i]))
    result_df.to_csv(parent_path + output_name, sep=',', encoding='utf-8')
    break

    

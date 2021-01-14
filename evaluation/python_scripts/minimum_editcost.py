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
        if(len(filenames) == 0):
            continue
        output_name = '_'.join(filenames[0].split('_')[1:-1]) + '_minimum.csv'
        seeds = []
        parameter = []
        for i in range(0, len(filenames)):
            parameter_df = np.split(pd.read_csv(path + '/' + dir +'/'+ filenames[i]), [10], axis=1)[0]
            file_df = np.split(pd.read_csv(path + '/' + dir +'/'+ filenames[i]), [10], axis=1)[1]
            parameter.append(parameter_df)
            seeds.append(file_df)
        df = seeds[0]
        indf = parameter[0]
        for i in range(1, len(seeds)):
            df = pd.concat((df, seeds[i]), ignore_index = True)
            indf = pd.concat((indf, parameter[i]), ignore_index = True)
        minimum_list = df.apply(pd.to_numeric).idxmin(axis=0)  
        output_df = df.iloc[[minimum_list[1]]]
        output_df = indf.join(output_df, how = 'right')
        del output_df['Unnamed: 0']
        result.append(output_df)
    result_df = result[0]
    for i in range(1, len(result)):
        result_df = pd.concat((result_df, result[i]))
    result_df.to_csv(parent_path + output_name, sep=',', encoding='utf-8')
    break

    

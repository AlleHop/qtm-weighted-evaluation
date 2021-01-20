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
    result_init = []
    result_seed = []
    for dir in dirs:
        filenames = []
        for file in os.listdir(path + '/' + dir):
            filenames.append(file)
        if(len(filenames) == 0):
            continue
        output_name_init = '_'.join(filenames[0].split('_')[1:-1]) + '_var_init.csv'
        output_name_seed = '_'.join(filenames[0].split('_')[1:-1]) + '_var_seed.csv'
        seeds = []
        for i in range(0, len(filenames)):
            file_df = pd.read_csv(path + '/' + dir +'/'+ filenames[i])
            seeds.append(file_df)
        df = seeds[0]
        for i in range(1, len(seeds)):
            df = pd.concat((df, seeds[i]), ignore_index = True)
        output_df = df[(df['maxIterations'] == 400 ) &  (df['plateauSize'] == 100) ].drop(columns=['sortPaths','randomness','insertEditCost','removeEditCost'])

        #mean = output_df.groupby('initialization')[['editsWeight','edits', 'time']].std(ddof=0)
        mean_init = output_df.groupby('initialization')[['editsWeight','edits', 'time']].mean()
        mean_seed = output_df.groupby('seed')[['editsWeight','edits', 'time']].mean()
        std_init = output_df.groupby('initialization')[['editsWeight','edits', 'time']].std(ddof=0)
        std_seed = output_df.groupby('seed')[['editsWeight','edits', 'time']].std(ddof=0)
        min_init = output_df.groupby('initialization')[['editsWeight','edits', 'time']].min()
        min_seed = output_df.groupby('seed')[['editsWeight','edits', 'time']].min()
        output_df_init = output_df.drop(columns=['time','edits','editsWeight','usedIterations', 'actualPlateau', 'seed'])
        output_df_init = output_df_init.join(min_init, on='initialization', how = 'inner').join(mean_init, on='initialization',lsuffix='Min', how = 'inner').join(std_init, on='initialization',lsuffix='Mean',rsuffix='Std', how = 'inner')
        output_df_init = output_df_init.drop_duplicates(subset= ['graph', 'initialization'])
        output_df_seed = output_df.drop(columns=['time','edits','editsWeight','usedIterations', 'actualPlateau', 'initialization'])
        output_df_seed = output_df_seed.join(min_seed, on='seed', how = 'inner').join(mean_seed, on='seed',lsuffix='Min', how = 'inner').join(std_seed, on='seed',lsuffix='Mean',rsuffix='Std', how = 'inner')
        output_df_seed = output_df_seed.drop_duplicates(subset= ['graph', 'seed'])
        output_df_init['WeightVariantionCoefficient'] = output_df_init['editsWeightStd'] / output_df_init['editsWeightMean'].replace({ 0 : 1 })
        output_df_seed['WeightVariantionCoefficient'] = output_df_seed['editsWeightStd'] / output_df_seed['editsWeightMean'].replace({ 0 : 1 })
        del output_df_init['Unnamed: 0']
        del output_df_seed['Unnamed: 0']
        result_init.append(output_df_init)
        result_seed.append(output_df_seed)
    result_df_init = result_init[0]
    result_df_seed = result_seed[0]
    for i in range(1, len(result_init)):
        result_df_init = pd.concat((result_df_init, result_init[i]))
        result_df_seed = pd.concat((result_df_seed, result_seed[i]))
    result_df_init.to_csv(parent_path + output_name_init, sep=',', encoding='utf-8')
    result_df_seed.to_csv(parent_path + output_name_seed, sep=',', encoding='utf-8')
    break

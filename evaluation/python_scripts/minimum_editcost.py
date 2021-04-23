import os
import pandas as pd
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
        for i in range(0, len(filenames)):
            file_df = pd.read_csv(path + '/' + dir +'/'+ filenames[i])
            seeds.append(file_df)
        df = seeds[0]
        for i in range(1, len(seeds)):
            df = pd.concat((df, seeds[i]), ignore_index = True)
        output_df = df[(df['maxIterations'] == 400 ) &  (df['plateauSize'] == 100) ].drop(columns=['insertEditCost','removeEditCost', 'maxIterations', 'plateauSize'])
        output_df = output_df[output_df.editsWeight == output_df.editsWeight.min()]
        output_df = output_df.iloc[[0]]

        del output_df['Unnamed: 0']
        result.append(output_df)
    result_df = result[0]
    for i in range(1, len(result)):
        result_df = pd.concat((result_df, result[i]))
    result_df.to_csv(parent_path + output_name, sep=',', encoding='utf-8')
    break

    

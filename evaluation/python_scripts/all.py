import os
import pandas as pd
import argparse


parser = argparse.ArgumentParser(prog='all.py')
parser.add_argument('-p', '--path')
parser.add_argument('-i', '--insert', default=1, type=int)
parser.add_argument('-r', '--remove', default=1, type=int)


args = vars(parser.parse_args())
path = args['path']
insert = args['insert']
remove = args['remove']

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
        if insert == remove and insert ==1:
            output_name = '_'.join(filenames[0].split('_')[1:-1]) + '_all.csv'
        else:
            output_name = '_'.join(filenames[0].split('_')[1:-1]) +'_i' + str(insert)+ 'r' +str(remove)+'_all.csv'
        seeds = []
        for i in range(0, len(filenames)):
            file_df = pd.read_csv(path + '/' + dir +'/'+ filenames[i])
            seeds.append(file_df)
        df = seeds[0]
        for i in range(1, len(seeds)):
            df = pd.concat((df, seeds[i]), ignore_index = True)
        df = df[df.iteration +1 == df.usedIterations]
        df = df[(df.insertEditCost == insert) & (df.removeEditCost == remove) ]
        #output_df = df.drop(columns=['insertEditCost','removeEditCost', 'maxIterations', 'plateauSize'])
        output_df = df
        if "unweighted" in filenames[i]:
            output_df['initialization'] = 'QTM-' + output_df['initialization'].astype(str)
        else:
            output_df['initialization'] = 'QTM-nonuniform-' + output_df['initialization'].astype(str)
        output_df['initialization'] = output_df['initialization'].str.replace("_", "-")

        #output_df['initialization'] = output_df['initialization'].astype(str) + output_df['sortPaths'].astype(str)
        #output_df['initialization'] = output_df['initialization'].str.replace("False", "-no-sort").str.replace("True", "-sort")

        #output_df['initialization'] = output_df['initialization'].astype(str) + output_df['sortPaths'].astype(str)
        #output_df['initialization'] = output_df['initialization'].str.replace("False", "-no-random").str.replace("True", "-random")

        output_df['initialization'] = output_df['initialization'].astype(str) + output_df['subtreeMove'].astype(str)
        output_df['initialization'] = output_df['initialization'].str.replace("False", "-no-subtree").str.replace("True", "-subtree")

        output_df['initialization'] = output_df['initialization'].astype(str) + output_df['subtreeSortPaths'].astype(str)
        output_df['initialization'] = output_df['initialization'].str.replace("False", "").str.replace("True", "-sort")

        output_df = output_df.rename({'initialization': 'algorithm'}, axis=1)
        del output_df['Unnamed: 0']
        result.append(output_df)
    result_df = result[0]
    for i in range(1, len(result)):
        result_df = pd.concat((result_df, result[i]))
    result_df.to_csv(parent_path + output_name, sep=',', encoding='utf-8')
    break

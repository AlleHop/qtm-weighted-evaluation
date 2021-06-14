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
        df = df[df.iteration +1 == df.usedIterations]
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
        #output_df = df.drop(columns=['sortPaths','randomness','insertEditCost','removeEditCost'])
        #mean = output_df.groupby('initialization')[['editCosts','edits', 'time']].std(ddof=0)
        mean_init = output_df.groupby('initialization')[['editCosts','edits', 'time']].mean()
        mean_seed = output_df.groupby('seed')[['editCosts','edits', 'time']].mean()
        std_init = output_df.groupby('initialization')[['editCosts','edits', 'time']].std(ddof=0)
        std_seed = output_df.groupby('seed')[['editCosts','edits', 'time']].std(ddof=0)
        min_init = output_df.groupby('initialization')[['editCosts','edits', 'time']].min()
        min_seed = output_df.groupby('seed')[['editCosts','edits', 'time']].min()
        output_df_init = output_df.drop(columns=['time','edits','editCosts','usedIterations', 'actualPlateau', 'seed'])
        output_df_init = output_df_init.join(min_init, on='initialization', how = 'inner').join(mean_init, on='initialization',lsuffix='Min', how = 'inner').join(std_init, on='initialization',lsuffix='Mean',rsuffix='Std', how = 'inner')
        output_df_init = output_df_init.drop_duplicates(subset= ['graph', 'initialization'])
        output_df_seed = output_df.drop(columns=['time','edits','editCosts','usedIterations', 'actualPlateau', 'initialization'])
        output_df_seed = output_df_seed.join(min_seed, on='seed', how = 'inner').join(mean_seed, on='seed',lsuffix='Min', how = 'inner').join(std_seed, on='seed',lsuffix='Mean',rsuffix='Std', how = 'inner')
        output_df_seed = output_df_seed.drop_duplicates(subset= ['graph', 'seed'])
        output_df_init['WeightVariantionCoefficient'] = output_df_init['editCostsStd'] / output_df_init['editCostsMean'].replace({ 0 : 1 })
        output_df_seed['WeightVariantionCoefficient'] = output_df_seed['editCostsStd'] / output_df_seed['editCostsMean'].replace({ 0 : 1 })
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

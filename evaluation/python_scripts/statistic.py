import os
import networkit as nk
import pandas as pd
import argparse


parser = argparse.ArgumentParser(prog='statistic.py')
parser.add_argument('-p', '--path')

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
        df['solved'] = df['solved'].astype(str)
        df['solved'] = df['solved'].replace({True: 'True', False: 'True', '-1': 'False'})
        #df = df['solved'].replace({True: 'True', False: 'True', "-1": 'False'})
        output_df["number graphs"] = len(df)
        output_df["exact solution given"] = len(df[df.solved == "True"])
        output_df["lower bound given"] = len(df[(df.solved != "True") & (df.solution_cost >= 0)])
        output_df["no exact solution given"] = len(df[~(df.solved == "True")])
        output_df["exact solved by QTM"] = len(df[df.ratio == 1.0])
        output_df["exact solved by subtreeMove"] = len(df[(df.ratio == 1.0) & (df.subtreeMove == True)])
        output_df["exact solved by subtreeSortPath"] = len(df[(df.ratio == 1.0) & (df.subtreeSortPaths == True)])
        output_df["max 5% worse than exact"] = len(df[(df.ratio > 1.0) & (df.ratio <= 1.05) & (df.solved == 'True')])
        output_df["more than 5% worse"] = len(df[(df.ratio > 1.05) & (df.solved == 'True')])
        output_df["error ratio > 1.0?"] = len(df[(df.ratio < 1.0) & (df.solved == 'True')])
        output_df["max ratio"] = df['ratio'].max()
        output_df["noexact best solution subtreemove"] = len(df[(df.solved != "True") & (df.subtreeMove == True)])
        output_df["noexact best solution subtreesort"] = len(df[(df.solved != "True") & (df.subtreeSortPaths == True)])
        output_df["best solution subtreemove"] = len(df[(df.subtreeMove == True)])
        output_df["best solution subtreesort"] = len(df[ (df.subtreeSortPaths == True)])
        print(df[(df.ratio < 1.0) & (df.solved == 'True')])
        print(output_df)
        #del output_df['Unnamed: 0']
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_df.to_csv(output_path + file.strip("_"), sep=',', encoding='utf-8')


    

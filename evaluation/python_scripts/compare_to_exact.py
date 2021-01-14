import sys, getopt
import os
import networkit as nk
import timeit
import pandas as pd
import numpy as np
import argparse


parser = argparse.ArgumentParser(prog='compare_to_exact.py')
parser.add_argument('qtm', help='First File qtm')
parser.add_argument('exact', help='Second File exact')

args = vars(parser.parse_args())
qtm = args['qtm']
exact = args['exact']

qtm_df = pd.read_csv(qtm)
exact_df = pd.read_csv(exact)
qtm_df = qtm_df.set_index(['graph_index'])
exact_df = exact_df.set_index(['graph_index'])
graph_names = exact_df[['path']]

qtm_df = qtm_df.drop(columns=['maxIterations','sortPaths','randomness','plateauSize','insertEditCost','removeEditCost','edits'])
exact_df = exact_df.drop(columns=['multiplier','permutation','forbidden_subgraphs','edits','path'])
output_df = qtm_df.merge(exact_df, on='graph_index', how='outer' ).fillna(value= -1).sort_values(['graph_index'])
output_df.insert(len(output_df.columns), 'ratio', 0.0)
output_df = output_df.astype({'editsWeight' : 'int64','usedIterations' : 'int64','actualPlateau': 'int64', 'n': 'int64', 'solution_cost': 'int64'})
for index, row in output_df.iterrows():
    num = row[['graph']]
    #if(not(isinstance(num, str))):
    #    output_df['graph'][index] = graph_names['path'][index].strip('data/').strip('bio').strip('/').strip('.graph')
    #   output_df['n'][index] = graph_names['path'][index].split('-')[4].strip('.graph')
    if(output_df['solution_cost'][index]== -1):
        output_df['ratio'][index]= -1
    elif(output_df['editsWeight'][index]== -1):
        output_df['ratio'][index]= -2
    elif(output_df['solution_cost'][index]== 0):
        if(output_df['editsWeight'][index]!= 0):
            output_df['ratio'][index]= -3
        else:
            output_df['ratio'][index]= 1
    else:
        ratio = output_df['editsWeight'][index] / output_df['solution_cost'][index] 
        if(ratio< 1):
            output_df['ratio'][index] = 1
        else:
            output_df['ratio'][index] = ratio
output_df.to_csv(".." + qtm.strip(".csv") + '_compare.csv', sep=',', encoding='utf-8')


    

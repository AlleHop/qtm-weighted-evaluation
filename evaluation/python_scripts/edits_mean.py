import os
import pandas as pd
import argparse


parser = argparse.ArgumentParser(prog='path')
parser.add_argument('-p', '--path')

args = vars(parser.parse_args())
path = args['path']

result = []
df = pd.read_csv(path)

df = df.groupby(['graph','algorithm']).mean()
#df = df.groupby(['graph','subtreeMove','subtreeSortPaths']).first().reset_index()

output_df = df
del output_df['Unnamed: 0']
#print(output_df)
#output_df.to_csv(path.strip(".csv") + '_edits.csv', sep=',', encoding='utf-8')
output_df.to_csv('../../remote_output/output_bugsubtreesort/QTM_big/facebook/ratio_i1r2_mean.csv', sep=',', encoding='utf-8')

import os
import pandas as pd
import argparse


parser = argparse.ArgumentParser(prog='path')
parser.add_argument('-p', '--path')

args = vars(parser.parse_args())
path = args['path']

result = []
df = pd.read_csv(path)
if(df['removeEditCost'][1]>df['insertEditCost'][1]):
    df['insertEdits'] = df['edits'] - df['editCosts'] + df['edits']
    df['removeEdits'] = df['editCosts'] - df['edits']
    df['ratioRemove'] = df['removeEdits'] / df['edits']
    df['ratioInsert'] = df['insertEdits'] / df['edits']
if(df['removeEditCost'][1]<df['insertEditCost'][1]):
    df['insertEdits'] = df['editCosts'] - df['edits']
    df['removeEdits'] = df['edits'] - df['insertEdits']
    df['ratioRemove'] = df['removeEdits'] / df['edits']
    df['ratioInsert'] = df['insertEdits'] / df['edits']
output_df = df
del output_df['Unnamed: 0']
#print(output_df)
#output_df.to_csv(path.strip(".csv") + '_edits.csv', sep=',', encoding='utf-8')
output_df.to_csv('../../remote_output/output_bugsubtreesort/QTM_big/facebook/ratio_i2r1_edits.csv', sep=',', encoding='utf-8')

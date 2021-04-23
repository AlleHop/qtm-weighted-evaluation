import os
import pandas as pd
import argparse


parser = argparse.ArgumentParser(prog='sort.py')
parser.add_argument('-p', '--path')

args = vars(parser.parse_args())
path = args['path']

parent_path = '/'.join(path.split('/')[:-2]) + '/'
output_path = path + "sorted/"
result = []
for file in os.listdir(path):
    if file.endswith(".csv"):
        df = pd.read_csv(path + "/"+ file)
        index = []
        for i, row in df.iterrows():
            parts = row['graph'].split('-')
            index.append(int(parts[2]))
        df.insert(0,'graph_index', index)
        output_df = df.sort_values('graph_index')
        output_df = output_df.set_index(['graph_index'])
        #del output_df['Unnamed: 0']
        #print(output_df)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_df.to_csv(output_path + file.strip(".csv") + '_sorted.csv', sep=',', encoding='utf-8')


    

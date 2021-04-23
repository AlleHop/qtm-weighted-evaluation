import os
import pandas as pd
import argparse


parser = argparse.ArgumentParser(prog='bionames.py')
parser.add_argument('-l', '--limit', type=int)
args = vars(parser.parse_args())
limit = int(args['limit'])

list = open('bio' + str(limit) + '.txt', 'w+')
input_df = pd.read_csv('../input/biological/bio_data.csv')
for index, row in input_df.iterrows():
    if(int(row['k']) >= limit):
        list.write("biological/graphs/" + row['Graph'].split('.')[0] + ".graph\n")
list.close()

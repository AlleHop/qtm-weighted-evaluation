#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

parser = argparse.ArgumentParser(prog='performance_plot.py')
parser.add_argument('-p', '--path')
args = vars(parser.parse_args())
path = args['path']

if __name__ == '__main__':
    #exact_df = pd.read_csv('bio_exact_data.csv')
    #graphs_mink_20 = set(exact_df[exact_df.k > 19].Graph.to_list())
    #print(len(graphs_mink_20))

    df = pd.concat([pd.read_csv(path + f) for f in [
        #       'fb_results-all-aggregated.csv',
        #       'bio_results-all-aggregated.csv'
        'biosubtreeMove_all_dataset.csv',
        'biounweighted_all_dataset.csv'
        #'unweighted_all_dataset.csv'
        #'biounweighted_all_nochanges.csv',
        #'unweighted_all_nochanges.csv'
        # 'large_results-aggregated.csv',
        # 'generated_results-aggregated.csv'
    ]])

    df.loc[df.Dataset == 'facebook', 'Dataset'] = 'Facebook 100'
    df.loc[df.Dataset == 'biological', 'Dataset'] = 'COG uniform'
    df.loc[df.Dataset == 'biononuniform', 'Dataset'] = 'COG nonuniform'
    df = df[(df.edits >= 20) | (df.Dataset == 'Facebook 100')]
    df = df[(df['algorithm'].str.contains('no-init')) | (df['algorithm'].str.contains('edit-init'))]
    df['algorithm'] = df['algorithm'].str.replace("-nonuniform", "")
    #df = df[(df.Graph.isin(graphs_mink_20) | (df.Dataset == 'Facebook 100')) & ~df['Algorithm'].str.contains('c-min')]
    algorithm_order = sorted(df.algorithm.unique(), key=lambda x : x[::-1])

    fig, ax = plt.subplots(1, figsize=(9, 4))
    g = sns.boxplot(y='algorithm', x='Iterations', hue='Dataset', data=df, order=algorithm_order, ax=ax, whis=[5, 95], boxprops={'linewidth': 0})
    g.set(xscale='log')
    ax.grid(b=True, axis='x', which='both', ls='dashed')
    ax.legend
    plt.savefig(path +'plot/'+ 'facebook_nochanges_iterations.pdf', bbox_inches='tight')

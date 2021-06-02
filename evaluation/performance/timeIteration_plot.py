#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as grd
import seaborn as sns
import argparse
import os

parser = argparse.ArgumentParser(prog='timeIteration_plot.py')
parser.add_argument('-p', '--path')

args = vars(parser.parse_args())
path = args['path']

def algorithm_style(algorithm):
    if "nonuniform" in algorithm:
        return "."
    return "."

my_algo_colors = sns.color_palette(n_colors=6)

def algorithm_color(algorithm):
    if "sort" in algorithm:
        return my_algo_colors[2]
    if "no-subtree" in algorithm:
        return my_algo_colors[3]
    if "subtree" in algorithm:
        return my_algo_colors[1]
    assert False

def algorithm_color_combine(algorithm):
    if "COG" in algorithm:
        if "sort" in algorithm:
            return my_algo_colors[2]
        if "no-subtree" in algorithm:
            return my_algo_colors[3]
        if "subtree" in algorithm:
            return my_algo_colors[1]
    if "facebook" in algorithm:
        if "sort" in algorithm:
            return my_algo_colors[4]
        if "no-subtree" in algorithm:
            return my_algo_colors[4]
        if "subtree" in algorithm:
            return my_algo_colors[5]
    assert False


def plot_with_buckets(df):
    bb = [10, 100, 1000, df['m'].max() * 1.01]
    nbuckets = len(bb) - 1

    fig = plt.figure(figsize=(9, 3))
    gs = grd.GridSpec(nrows=1, ncols=nbuckets, wspace=0.0, hspace=0.0,
                      width_ratios=[1.0 / nbuckets for i in range(nbuckets)])
    axes = [plt.subplot(g) for g in gs]
    for ax in axes[1:]:
        ax.set_yticklabels(ax.get_yticklabels(), visible=False)
        ax.yaxis.set_ticks_position('none')

    for algo, values in df.groupby('algorithm'):
        for ax in axes:
            lines = ax.scatter(values['m'], values['Time per Edge'], label=algo,
                            color=algorithm_color(algo),
                            marker=algorithm_style(algo))
            max_fraction = values['m'].max()
            if max_fraction < 1:
                max_ratio = values['Ratio'].max()
                ax.scatter([max_ratio], [max_fraction],
                           color=lines[0].get_color(), marker='x')

    #axes[0].legend(ncol=3, fancybox=False, frameon=False, loc='upper left',
    #               bbox_to_anchor=(-0.16, -0.15))
    axes[-1].legend(loc='lower right')
    for i in range(nbuckets):
        axes[i].set_xlim(bb[i], bb[i+1])
        # axes[i].set_ylim(0.99, 1.001)
        axes[i].grid(b=True, axis='both', which='major', ls='dashed')

    axes[0].set_xticks([10, 50, 100])
    axes[1].set_xticks([500, 1000])

    axes[0].set_ylabel('Time per iteration and edge  [in \u03BCs]')
    axes[nbuckets//2].set_xlabel('Number of edges')
    return fig


def plot_simple(df):
    fig, ax = plt.subplots(1, figsize=(9, 3))
    for algo, values in df.groupby('algorithm'):
        ax.scatter(values['m'], values['Time per Edge'], label=algo,
                color=algorithm_color(algo), marker=algorithm_style(algo), s=5)
    ax.grid(b=True, axis='both', which='major', ls='dashed')
    ax.legend()
    ax.set_ylabel('Time per iteration and edge  [in \u03BCs]')
    ax.set_xlabel('Number of edges')
    ax.set_xscale('log')
    return fig

def plot_simple_combine(df):
    fig, ax = plt.subplots(1, figsize=(9, 3))
    for algo, values in df.groupby('algorithm'):
        ax.scatter(values['m'], values['Time per Edge'], label=algo,
                color=algorithm_color_combine(algo), marker=algorithm_style(algo), s=5)
    ax.grid(b=True, axis='both', which='major', ls='dashed')
    ax.legend()
    ax.set_ylabel('Time per iteration and edge  [in \u03BCs]')
    ax.set_xlabel('Number of edges')
    ax.set_xscale('log')
    return fig

if __name__ == '__main__':
    for result_name in [
                        'biosubtreeMove_time.csv',
                        'biounweighted_time.csv',
                        'unweighted_time.csv',
                        'ratio_time.csv',
                        'combine.csv'
                    ]:

        if not os.path.isfile(path + result_name) and result_name != "combine.csv" :
            continue
        if result_name == "combine.csv":
            if not os.path.isfile(path + 'biounweighted_time.csv'):
                continue
            if not os.path.isfile(path + 'unweighted_time.csv'):
                continue
            a = pd.read_csv(path + 'unweighted_time.csv')
            a['algorithm'] = a['algorithm'].str.replace("QTM", "facebook100")
            b = pd.read_csv(path + 'biounweighted_time.csv')
            b['algorithm'] = b['algorithm'].str.replace("QTM", "COG similarity")
            d = pd.concat([a,b])
        else :
            d = pd.read_csv(path + result_name)


        all_algorithms = d['algorithm'].unique()

        algorithm_sets = {
            'all' : all_algorithms,
            #'sorting' : {algo for algo in all_algorithms if 'init-sort-no-random' in algo},
            #'sorting-random' : {algo for algo in all_algorithms if 'init-sort-random' in algo},
            #'variants' : {algo for algo in all_algorithms if 'no-init' in algo or 'edit-init' in algo}
            }

        for set_name, algorithms in algorithm_sets.items():
            filtered_df = d[d['algorithm'].isin(algorithms)].copy()

            if len(filtered_df) == 0:
                continue

            filtered_df['Best unweighted k'] = filtered_df.groupby(['graph'])['edits'].transform(np.min)
            filtered_df = filtered_df[filtered_df['Best unweighted k'] > 20]

            plot_df = filtered_df
            print(plot_df['Time per Edge'].max())

            if result_name == "combine.csv":
                fig = plot_simple_combine(plot_df)
            else:    
                fig = plot_simple(plot_df)
            
            output_path = path + '/plot/' 
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            fig.savefig(output_path + result_name.replace('.csv',
                                            '-time-iteration-{}.pdf'.format(set_name)),
                        bbox_inches='tight')

#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as grd
import seaborn as sns
import argparse
import os

parser = argparse.ArgumentParser(prog='performance_plot.py')
parser.add_argument('-p', '--path')
parser.add_argument('-e', '--exact', help='exact solution', default="", type=str)

args = vars(parser.parse_args())
path = args['path']
exact= args['exact']


def algorithm_style(algorithm):
    #if "no-sort-no-random-subtree" in algorithm:
    #   return "--"
    #if "no-sort-no-random-no-subtree" in algorithm:
    #   return "-."
    #if "no-sort-random-subtree" in algorithm:
    #    return "--"
    #if "no-sort-random-no-subtree" in algorithm:
    #   return "-."
    #if "sort-no-random-subtree" in algorithm:
    #   return "--"
    #if "sort-no-random-no-subtree" in algorithm:
    #   return "-."
    #if "sort-random-subtree" in algorithm:
    #  return ":"
    #if "sort-random-no-subtree" in algorithm:
    #   return "-"
    if "no-subtree" in algorithm:
        return "-"
    if "subtree" in algorithm:
       return ":"
    return "-"


my_algo_colors = sns.color_palette(n_colors=5)


def algorithm_color(algorithm):
    if "asc-min-init" in algorithm:
        return my_algo_colors[2]
    if "desc-min-init" in algorithm:
        return my_algo_colors[3]
    if "edit-init" in algorithm:
        return my_algo_colors[1]
    if "no-init" in algorithm:
        return my_algo_colors[0]
    if "rand-min-init" in algorithm:
        return my_algo_colors[4]
    assert False


def get_fraction_ratio_df(d, key='Perf. Ratio'):
    # max_value = d[key][d[key] != np.inf].max()
    output = []
    for algo, values in d.groupby('algorithm'):
        last_ratio = 0
        for i, r in enumerate(values[key].sort_values()):
            if last_ratio != r:
                if last_ratio > 0 and not np.isinf(r):
                    output.append((algo, i / len(values), last_ratio))
                    output.append((algo, i / len(values), r))
                last_ratio = r
        if not np.isinf(last_ratio):
            output.append((algo, 1, last_ratio))

    return pd.DataFrame(data=output,
                        columns=["algorithm", "Fraction", "Ratio"])


def plot_with_buckets(df):
    bb = [0.995, 1.1, 2, df['Ratio'].max() * 1.01]
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
            lines = ax.plot(values['Ratio'], values['Fraction'], label=algo,
                            color=algorithm_color(algo),
                            linestyle=algorithm_style(algo))
            max_fraction = values['Fraction'].max()
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

    axes[0].set_xticks([1, 1.05, 1.1])
    axes[1].set_xticks([1.5, 2.0])

    axes[0].set_ylabel('Fraction of instances')
    axes[nbuckets//2].set_xlabel('Performance ratio')
    return fig


def plot_simple(df):
    fig, ax = plt.subplots(1, figsize=(9, 3))
    for algo, values in df.groupby('algorithm'):
        ax.plot(values['Ratio'], values['Fraction'], label=algo,
                color=algorithm_color(algo), linestyle=algorithm_style(algo))
        max_fraction = values['Fraction'].max()
        if max_fraction < 1:
            max_ratio = values['Ratio'].max()
            ax.scatter([max_ratio], [max_fraction],
                       color=algorithm_color(algo), marker='x')
    ax.grid(b=True, axis='both', which='major', ls='dashed')
    #ax.legend(ncol=3, fancybox=False, frameon=False, loc='upper left',
    #          bbox_to_anchor=(-0.06, -0.15))
    ax.legend()
    ax.set_ylabel('Fraction of instances')
    ax.set_xlabel('Performance ratio')
    return fig


def transform_input(df):
    s = df.set_index(['graph', 'algorithm', 'seed'])
    d = s.unstack().reset_index()
    d.columns = pd.Index([v if v else k for k, v in d.columns.to_list()])
    return d


if __name__ == '__main__':
    for result_name in [#'fb_results-all-aggregated.csv',
                        'biomatrix_all.csv',
                        'biosubtreeMove_all.csv',
                        #'large_results-aggregated.csv',
                        #'generated_results-aggregated.csv'
                        ]:
                        # 'bio_with_20_iterations.csv']:
        d = { 'graph':['none'], 'solution_cost':[-1]}
        exact_solution = pd.DataFrame(d,columns=['graph','solution_cost'])

        if(exact != ""):
            exact_solution = pd.read_csv(exact)
            exact_solution['path'] = exact_solution['path'].str.replace("data/bio/", "").str.replace(".graph", "")
            exact_solution = exact_solution.rename({'path': 'graph'}, axis=1).drop(columns=['multiplier', 'permutation', 'edits', 'time_exact', 'forbidden_subgraphs', 'graph_index', 'solved'])
            exact_solution = exact_solution.set_index(['graph'])
            #print(exact_solution)
            #print(exact_solution[exact_solution['graph'] == 'bio-nr-3212-size-5'])
        
        d = pd.read_csv(path + result_name)
        d['Best k'] = d.groupby(['graph'])['editsWeight'].transform(np.min)
        assert ((d['Best k'] <= d['editsWeight']) | d['editsWeight'].isna()).all()
        d['Best unweighted k'] = d.groupby(['graph'])['edits'].transform(np.min)
        assert ((d['Best unweighted k'] <= d['edits']) | d['edits'].isna()).all()

        # d['Ratio'] = d['Best k'] / d['Edits']

        # fig, ax = plt.subplots(1, figsize=(10, 6))
        # for algo, values in d.groupby('Algorithm'):
        #     ax.plot(range(1, len(values) + 1),
        #             list(values['Ratio'].sort_values()), label=algo)
        # ax.legend()
        # ax.set_xscale('log')

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

            filtered_df['exact'] = filtered_df.groupby(['graph'])['editsWeight'].transform(lambda x : exact_solution[x.name] if x.name in exact_solution else np.nan)
            #print(filtered_df)
            filtered_df['Best filtered k'] = filtered_df.groupby(['graph'])['editsWeight'].transform(np.min)
            assert ((filtered_df['Best filtered k'] <= filtered_df['editsWeight']) | filtered_df['editsWeight'].isna()).all()
            filtered_df['Best filtered unweighted k'] = filtered_df.groupby(['graph'])['edits'].transform(np.min)
            assert ((filtered_df['Best filtered unweighted k'] <= filtered_df['edits']) | filtered_df['edits'].isna()).all()

            # if 'with_20' in result_name:
            #     filtered_df['Perf. Ratio'] = filtered_df['Edits 20'] / filtered_df['Best filtered k']
            #     filtered_df.loc[(filtered_df['Edits 20'] == filtered_df['Best filtered k']), 'Perf. Ratio'] = 1.0
            # else:
            filtered_df['Perf. Ratio'] = filtered_df['editsWeight'] / filtered_df['Best filtered k']
            filtered_df.loc[(filtered_df['editsWeight'] == filtered_df['Best filtered k']), 'Perf. Ratio'] = 1.0
            # filtered_df.loc[((filtered_df['Best k'] == 0) & (filtered_df['Edits'] > 0)), 'Perf. Ratio'] = 100

            plot_df = get_fraction_ratio_df(filtered_df)
            #print(plot_df['Ratio'].max())
            if plot_df['Ratio'].max() > 3:
                fig = plot_with_buckets(plot_df)
            else:
                fig = plot_simple(plot_df)
            
            output_path = path + '/plot/' 
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            fig.savefig(output_path + result_name.replace('.csv',
                                            '-edits-performance-{}.pdf'.format(set_name)),
                        bbox_inches='tight')

            if "bio" in result_name:
                plot_df = get_fraction_ratio_df(filtered_df[filtered_df['Best k'] > 0])

                if plot_df['Ratio'].max() > 3:
                    fig = plot_with_buckets(plot_df)
                else:
                    fig = plot_simple(plot_df)

                fig.savefig(
                    output_path + result_name.replace('.csv',
                                        '-min-k-0-editsWeight-performance-{}.pdf'.format(set_name)),
                    bbox_inches='tight')

                plot_df = get_fraction_ratio_df(filtered_df[filtered_df['Best unweighted k'] > 20])

                if plot_df['Ratio'].max() > 3:
                    fig = plot_with_buckets(plot_df)
                else:
                    fig = plot_simple(plot_df)

                fig.savefig(
                    output_path + result_name.replace('.csv',
                                        '-min-k-20-edits-performance-{}.pdf'.format(set_name)),
                    bbox_inches='tight')

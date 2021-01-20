#!/usr/bin/env python3

import pandas as pd

if __name__ == '__main__':
    for result_name in [
            #'generated_results.csv',
            #'large_results.csv',
            #'fb_results-all.csv',
            'bio_results-all.csv'
    ]:

        df = pd.read_csv(result_name)
        s = df.set_index(['Dataset', 'Graph', 'Algorithm', 'Sample',
                          'Iteration', 'Name'])
        del df
        d = s.unstack().reset_index()
        del s
        d.columns = pd.Index([v if v else k for k, v in d.columns])

        summary_df = d[d['Iteration'] == -1].dropna(axis='columns').set_index(
            ['Dataset', 'Graph', 'Algorithm', 'Sample'], verify_integrity=True
        )

        del summary_df['Iteration']

        gb_20 = d[d['Iteration'] <= 20].groupby(
            ['Dataset', 'Graph', 'Algorithm', 'Sample']
        )

        summary_df['Edits 20'] = gb_20['edits'].min()
        summary_df['Time 20'] = gb_20['time'].sum()
        summary_df['Instructions 20'] = gb_20['instructions'].sum()

        d_initialization = d[d['Iteration'] == 0].set_index(
            ['Dataset', 'Graph', 'Algorithm', 'Sample'], verify_integrity=True
        )

        summary_df['Edits Initialization'] = d_initialization['edits']
        summary_df['Time Initialization'] = d_initialization['time']
        summary_df['Instructions Initialization'] = d_initialization['instructions']

        summary_df['Total Instructions'] = d[d['Iteration'] >= 0].groupby(
            ['Dataset', 'Graph', 'Algorithm', 'Sample']
        )['instructions'].sum()

        summary_df.to_csv(result_name.replace('.csv', '-aggregated.csv'))

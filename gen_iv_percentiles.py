import os

import numpy as np
import pandas as pd

from option_header import HvHeaders, PhvHeaders, IvMeanHeaders, IvCallHeaders, IvPutHeaders

percentiles = np.arange(0.01, 1.0, 0.01)


def get_iv_ranges():
    for file_name in os.listdir('options'):
        symbol = file_name.replace('.csv', '')
        if len(symbol) >= 5:
            continue
        print(symbol)
        df = pd.read_csv(f'options/{symbol}.csv')
        percentiles_df = df[HvHeaders + PhvHeaders + IvMeanHeaders + IvCallHeaders + IvPutHeaders].quantile(percentiles)
        percentiles_df = percentiles_df.reset_index().rename(columns={'index': 'Percentile'})
        percentiles_df.to_csv(f'option_percentiles/{symbol}.csv', index=False)


def get_all_iv_ranges_by_header():
    all_headers = HvHeaders + PhvHeaders + IvMeanHeaders + IvCallHeaders + IvPutHeaders
    percentiles_dfs = []
    for file_name in sorted(os.listdir('options')):
        symbol = file_name.replace('.csv', '')
        if len(symbol) >= 5:
            continue
        print(symbol)
        df = pd.read_csv(f'options/{symbol}.csv')
        percentiles_df = df[all_headers].quantile(percentiles)
        percentiles_dfs.append((symbol, percentiles_df))

    medians = {}
    means = {}
    for header in all_headers:
        print(header)
        dfs = {}
        for symbol, percentiles_df in percentiles_dfs:
            dfs[symbol] = percentiles_df[header]
        df = pd.DataFrame(dfs)
        df = df[sorted(df.columns)]
        mean = df.mean(axis=1)
        median = df.median(axis=1)
        means[header] = mean
        medians[header] = median
        df.insert(0, 'avg', mean)
        df.insert(0, 'medium', median)
        df = df.rename_axis('percentiles')
        resort_df = df.rename_axis('percentiles')
        resort_df.to_csv(f'option_headers/{header}.csv', index=True)

    means_df = pd.DataFrame(means)
    means_df = means_df[sorted(means_df.columns)]
    means_df = means_df.rename_axis('percentiles')
    means_df.to_csv(f'option_headers/means.csv', index=True)

    median_df = pd.DataFrame(medians)
    median_df = median_df[sorted(median_df.columns)]
    median_df = median_df.rename_axis('percentiles')
    median_df.to_csv(f'option_headers/median.csv', index=True)



get_iv_ranges()
import os

import numpy as np
import pandas as pd

from option_header import HvHeaders, PhvHeaders, IvMeanHeaders, IvCallHeaders, IvPutHeaders, TopHeaders, DayRanges
from src.utils.idx_utils import get_percentile_rank
from src.utils.path_utils import get_root_path, list_csv_names, get_data_path
from src.utils.utils import get_symbols_from_folders, get_future_hv

# https://data.nasdaq.com/tables/VOL/QUANTCHA-VOL/export

percentiles = np.arange(0.01, 1.0, 0.01)


def percentiles_iv_by_symbols():
    headers = list_csv_names(get_data_path(f'iv_percentiles_headers'))
    data_symbols = {}
    for header in headers:
        print(header)
        df = pd.read_csv(get_data_path(f'iv_percentiles_headers/{header}.csv'))
        for symbol in df.columns:
            if symbol not in data_symbols:
                data_symbols[symbol] = {}
            symbol_headers = data_symbols[symbol]
            symbol_headers[header] = df[symbol]

    for symbol, header_data in data_symbols.items():
        df = pd.DataFrame(header_data)
        df = df[sorted(df.columns)]
        df.rename_axis('percentiles', inplace=True)
        df.to_csv(get_data_path(f'iv_percentiles_symbols/{symbol}.csv'), index=True)


def get_all_iv_ranges_by_header():
    output_folder = get_data_path(f'iv_percentiles_headers')
    os.makedirs(output_folder, exist_ok=True)
    exist_headers = list_csv_names(output_folder)
    all_headers = [h for h in (HvHeaders + PhvHeaders + IvMeanHeaders + IvCallHeaders + IvPutHeaders) if h not in exist_headers]

    for header in all_headers:
        print(header)
        df = pd.read_csv(get_data_path(f'iv_all.csv'), usecols=['ticker', header])
        df.dropna(inplace=True)
        df.rename(columns={'ticker': 'symbol'}, inplace=True)
        all_df = df[[header]].quantile(percentiles)

        symbol_dfs = {}
        for symbol, symbol_df in df.groupby('symbol'):
            if len(symbol_df) >= 1000:
                tmp_df = symbol_df[[header]].quantile(percentiles)
                symbol_dfs[symbol] = tmp_df[header]
        df = pd.DataFrame(symbol_dfs)
        df = df[sorted(df.columns)]
        mean = df.mean(axis=1)
        median = df.median(axis=1)
        df.insert(0, 'all', all_df[header])
        df.insert(1, 'median', median)
        df.insert(2, 'mean', mean)
        df.rename_axis('percentiles', inplace=True)
        df.to_csv(get_data_path(f'iv_percentiles_headers/{header}.csv'), index=True)


def percentile_options():
    symbols = get_symbols_from_folders('option_percentiles')
    IV_HEADERS = HvHeaders + PhvHeaders + IvMeanHeaders + IvCallHeaders + IvPutHeaders
    for symbol in symbols:
        print(symbol)
        percentile_df = pd.read_csv(f'option_percentiles/{symbol}.csv')
        percentile_df.set_index('percentiles', inplace=True)
        option_df = pd.read_csv(f'options/{symbol}.csv')
        option_df = option_df[TopHeaders + IV_HEADERS]
        option_df['date'] = pd.to_datetime(option_df['date'])
        option_df.set_index('date', inplace=True)
        option_df.sort_index(inplace=True)
        for header in IV_HEADERS:
            option_df[f'{header}_rank'] = option_df.apply(lambda row: get_percentile_rank(row[header], percentile_df[header]), axis=1)
        for dayRange in DayRanges:
            option_df[f'fv{dayRange}'] = option_df.apply(lambda row: get_future_hv(row.name, dayRange, option_df[f'hv{dayRange}']), axis=1)
        for dayRange in DayRanges:
            option_df[f'dif_v{dayRange}'] = option_df[f'ivmean{dayRange}'] - option_df[f'fv{dayRange}']
        option_df.to_csv(f'option_percentiled/{symbol}.csv', index=True)


if __name__ == '__main__':
    get_all_iv_ranges_by_header()
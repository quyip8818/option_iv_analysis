import pandas as pd

from src.processor.option_header import DiffVHeader
from src.utils.utils import get_symbols_from_folders, get_percentile

OPTION_FOLDER = 'option_percentiled'


def get_option(symbol, group_by_day_name, percentiles):
    df = pd.read_csv(f'{OPTION_FOLDER}/{symbol}.csv')
    df = df[(df['next_report_days'] >= 10.0) & (df['pass_report_days'] >= 10.0)]
    df = df[['date', group_by_day_name] + DiffVHeader]
    df[group_by_day_name] = df.apply(lambda row: get_percentile(row[group_by_day_name], percentiles), axis=1)
    df.sort_values(by='date', ascending=False, inplace=True)
    # for header in PhvHeaders:
    #     df[header] = -df[header].diff()
    df.drop(columns=['date'], inplace=True)
    df.dropna(inplace=True)
    return df


def read_all_options(group_by_day_name, percentiles):
    dfs = []
    for symbol in get_symbols_from_folders(OPTION_FOLDER):
        print(symbol)
        df = get_option(symbol, group_by_day_name, percentiles)
        if len(df) > 100:
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


for header in ['ivmean10', 'ivmean30', 'ivmean90', 'ivmean180', 'ivmean1080']:
    percentile_df = pd.read_csv(f'option_headers/{header}.csv')
    percentiles = percentile_df['avg'].sort_values(ascending=True)
    group_by_day_name = header
    all_df = read_all_options(group_by_day_name, percentiles)
    grouped_df = all_df.groupby(group_by_day_name, as_index=False)
    median_df = grouped_df.median()
    median_df['count'] = grouped_df[group_by_day_name].count().values
    median_df[median_df['count'] >= 10000].to_csv(f'option_iv_value_analysis/{group_by_day_name}_diff_median.csv', index=False)

# mean_df = grouped_df.mean()
# mean_df['count'] = grouped_df[group_by_day_name].count().values
# mean_df[mean_df[group_by_day_name] <= 90].to_csv(f'option_fin_rep_date/{group_by_day_name}_diff_mean.csv', index=False)

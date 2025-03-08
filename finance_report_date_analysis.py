import pandas as pd

from option_header import IvMeanHeaders, HvHeaders, PhvHeaders, IvPutHeaders, IvCallHeaders
from utils import get_symbols_from_folders

OPTION_FOLDER = 'option_percentiled'

def get_option(symbol, group_by_day_name):
    df = pd.read_csv(f'{OPTION_FOLDER}/{symbol}.csv')
    df = df[['date', group_by_day_name] + IvMeanHeaders + HvHeaders + PhvHeaders + IvCallHeaders + IvPutHeaders]
    df.sort_values(by='date', ascending=False, inplace=True)
    # for header in PhvHeaders:
    #     df[header] = -df[header].diff()
    df.drop(columns=['date'], inplace=True)
    df.dropna(inplace=True)
    return df


def read_all_options(group_by_day_name):
    dfs = []
    for symbol in get_symbols_from_folders(OPTION_FOLDER):
        print(symbol)
        df = get_option(symbol, group_by_day_name)
        if len(df) > 100:
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


group_by_day_name = 'next_report_days'
all_df = read_all_options(group_by_day_name)
grouped_df = all_df.groupby(group_by_day_name, as_index=False)
# median_df = grouped_df.median()
# median_df['count'] = grouped_df[group_by_day_name].count().values
# median_df[median_df[group_by_day_name] <= 90].to_csv(f'option_fin_rep_date/{group_by_day_name}_rank_median.csv', index=False)
#
# mean_df = grouped_df.mean()
# mean_df['count'] = grouped_df[group_by_day_name].count().values
# mean_df[mean_df[group_by_day_name] <= 90].to_csv(f'option_fin_rep_date/{group_by_day_name}_rank_mean.csv', index=False)

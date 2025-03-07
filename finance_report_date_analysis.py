import os

import pandas as pd

from option_header import IvMeanHeaders, HvHeaders, PhvHeaders, IvPutHeaders, IvCallHeaders


def get_df(symbol, group_by_day_name):
    df = pd.read_csv(f'options/{symbol}.csv')
    df = df[['date', group_by_day_name] + IvMeanHeaders + HvHeaders + PhvHeaders + IvCallHeaders + IvPutHeaders]
    df.sort_values(by='date', ascending=False, inplace=True)
    # for header in PhvHeaders:
    #     df[header] = -df[header].diff()
    df.drop(columns=['date'], inplace=True)
    df.dropna(inplace=True)
    return df


def read_all_df(group_by_day_name):
    dfs = []
    for file_name in os.listdir('options'):
        symbol = file_name.replace('.csv', '')
        if len(symbol) >= 5:
            continue
        print(symbol)
        df = get_df(symbol, group_by_day_name)
        if len(df) > 100:
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


group_by_day_name = 'pass_report_days'
all_df = read_all_df(group_by_day_name)
grouped_df = all_df.groupby(group_by_day_name, as_index=False)
median_df = grouped_df.median()
median_df['count'] = grouped_df[group_by_day_name].count().values
median_df[median_df['count'] > 40000].to_csv(f'option_fin_report_date/{group_by_day_name}_median.csv', index=False)

# mean_df = grouped_df.mean()
# mean_df['count'] = grouped_df['next_report_days'].count().values
# mean_df[mean_df['count'] > 40000].to_csv('data/mean.csv', index=False)

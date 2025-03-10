import math
import os

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def get_symbols_from_folders(folder):
    symbols = [file_name.replace('.csv', '') for file_name in os.listdir(folder) if file_name.endswith('.csv')]
    return sorted([s for s in symbols if len(s) <= 5])


def get_percentile(value, percentiles: pd.Series):
    if value < percentiles.iloc[0]:
        return 0
    index = np.searchsorted(percentiles.values, value, side="left")
    return percentiles.index[index] if index < len(percentiles) else 1


def get_percentile_rank(value, percentiles):
    return math.floor(get_percentile(value, percentiles) * 100)


def get_next_date_str(date_str, day_diff):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    new_date = date + timedelta(days=day_diff)
    return new_date.strftime("%Y-%m-%d")


def get_date_value(date: pd.DatetimeIndex, values: pd.Series):
    idx = np.searchsorted(values.index, date, side='left')
    if idx < 0 or idx >= len(values):
        return None
    day_diff = (values.index[idx] - date).days
    if abs(day_diff) >= 3:
        return None
    return values.iloc[idx]


def get_future_hv(date, next_days, hvs: pd.Series):
    next_date = date + timedelta(days=next_days)
    return get_date_value(next_date, hvs)

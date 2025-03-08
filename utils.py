import math
import os

import numpy as np
import pandas as pd


def get_symbols_from_folders(folder):
    symbols = [file_name.replace('.csv', '') for file_name in os.listdir(folder) if file_name.endswith('.csv')]
    return sorted([s for s in symbols if len(s) <= 5])


def get_percentile(value, percentiles: pd.Series):
    index = np.searchsorted(percentiles.values, value, side="right")
    return percentiles.index[index] if index < len(percentiles) else 1


def get_percentile_rank(value, percentiles):
    return math.floor(get_percentile(value, percentiles) * 100)

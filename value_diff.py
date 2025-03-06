import pandas as pd

from option_header import TopHeaders, IvMeanHeaders

df = pd.read_csv('options/COST.csv')
df = df[TopHeaders + IvMeanHeaders]
df = df.sort_values('date', ascending=True)
for header in IvMeanHeaders:
    df[header] = df[header].diff()

df.to_csv("data/COST.csv", index=False)
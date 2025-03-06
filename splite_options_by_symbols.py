import pandas as pd

df = pd.read_csv('data/OptionHistory2.csv')
symbols = df['ticker'].unique()
symbols = [s for s in symbols if isinstance(s, str)]
symbols.sort()

for symbol in symbols:
    print(symbol)
    symbol_df = df[df['ticker'] == symbol]
    symbol_df = symbol_df.drop('ticker', axis=1)
    symbol_df = symbol_df.dropna(subset=[col for col in symbol_df.columns if col != 'next_report_days'])
    if len(symbol_df) >= 90:
        symbol_df.sort_values(by='date', ascending=True, inplace=True)
        symbol_df.to_csv(f'options/{symbol}.csv', index=False)

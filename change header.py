import pandas as pd
import numpy
from pathlib import Path

file_path = Path('D:/Projects/AUD forex/rates_table.csv')
f = pd.read_csv(file_path)
print (f.head())

#
g = f.rename(columns = {'SB DATE': 'BPI DATE', 'SB BUY': 'BPI BUY', 'SB SELL': 'BPI SELL',
                    'BPI DATE': 'SB DATE', 'BPI BUY': 'SB BUY', 'BPI SELL': 'SB SELL'})
print(g.head())

g.to_csv(file_path, index = False)

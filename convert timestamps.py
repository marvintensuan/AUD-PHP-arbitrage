import pandas as pd
from pathlib import Path
import dateutil.parser as dparser

file_path = Path('D:/Projects/AUD forex/rates_table.csv')
rates_file = pd.read_csv(file_path)

sb = rates_file['SB DATE']
bp = rates_file['BPI DATE']

for i in range(0, len(sb)):
    sb[i] = dparser.parse(sb[i], fuzzy = True, ignoretz = True)

for i in range(0, len(bp)):
    bp[i] = dparser.parse(bp[i], fuzzy = True, ignoretz = True)

rates_file['SB DATE'] = sb
rates_file['BPI DATE'] = bp

save_file = rates_file.to_csv(file_path, index = False)
import numpy as np
import os
import pandas as pd
import time
from Setup import root
import Support_function as Sf



last_report =[]
tick = []
for key, value in root.items():
    if len(key) ==3:
        lr = Sf.get_column_header_from_file(value, 2)
        last_report.append(lr)
        tick.append(key)

df =pd.read_csv(root.loc['General info', 'Path'])

_list = []
for t in tick:
    if t in df.iloc[:,1]:
        _list.append(t)
    else:
        _list.append(" ")
print(len(df.iloc[:,1]))
print(len(_list))

















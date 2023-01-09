import pandas as pd
import numpy as np
from BarnStructure import root, main_folder
import matplotlib as plt
import datetime

# Get frequently updating financial report, P/E >0 and average trading value >100ml VND
def get_zombie_free_list(__df):
    __temp = __df.xs('P/E', level=1)[get_current_quarter_title(2)]
    __temp = __temp[__temp > 0]
    _qualified = trading_value[(trading_value['Value'] > 100000) &
                               (trading_value.index.isin(__temp.index))]
    result = __df[__df.index.get_level_values(0).isin(_qualified.index)]
    return result.index.get_level_values(0).drop_duplicates()


def get_current_quarter_title(_delay=1):
    _today = datetime.date.today()
    year = _today.year
    quater = pd.Timestamp(_today).quarter-_delay

    return f'Q{quater} {year}'


def get_periods(_last_quater, _length):
    _col_list = deri[[col for col in deri if col.startswith('Q')]].columns
    for i in range(len(_col_list)):
        if _col_list[i] == _last_quater:
            return [_col_list[j] for j in range(i,i+_length)]


def positive_profit_for_consecutive_months(__df,__period):
    __temp = __df.xs('Net profit', level=1)[__period]
    __temp['Min'] = __temp.min(axis=1)
    __tickers = __temp[__temp['Min'] > 0].index.get_level_values(0)
    result = __df[__df.index.get_level_values(0).isin(__tickers)]
    return result


def stable_ROE_for_consecutive_months(__df,__period,__bottom_line=0.02):
    __temp = __df.xs('ROE', level=1)[__period]
    __temp['Min'] = __temp.min(axis=1)
    __tickers = __temp[__temp['Min'] >= __bottom_line].index.get_level_values(0)
    result = __df[__df.index.get_level_values(0).isin(__tickers)]
    return result


def positive_index_for_last_quater(__df,_last_quater,index):
    __df = __df.reset_index(level=1)
    __df = __df[['Indicator',_last_quater]]
    __index = __df[(__df['Indicator']==index) & (__df[_last_quater]>0)].index
    __df = __df[__df.index.isin(__index)]
    return __df

def show_result(__df):
    print(__df.reset_index(level=1).head(10))
    return __df.index.get_level_values(0)

'''
DECLARATION
'''

filter_folder ="D:/Filter"
deri_path = root.loc['vietstock_derivation', 'Path']
live_data_path = f'{main_folder}/temp_/live_data.csv'
trading_value = pd.read_csv(live_data_path,usecols=[0,3],index_col=0)
general_info = pd.read_csv(root.loc['General info', 'Path'], index_col=0)
deri = pd.read_csv(deri_path, index_col=[0, 1])
# Current quater -1
last_quarter = get_current_quarter_title()
# 05 consecutive quarter from last quater
period = get_periods(last_quarter, 5)

'''
RUN
'''
deri = deri[period]
deri = deri.loc[deri.index.get_level_values(0).isin(get_zombie_free_list(deri)),:]

filter_df = positive_profit_for_consecutive_months(deri, period)
filter_df = stable_ROE_for_consecutive_months(filter_df, period)
#filter_df = positive_index_for_last_quater(filter_df,"Q2 2021",'AGR Net Profit')
tickers = filter_df.index.get_level_values(0).drop_duplicates()
results = general_info[general_info.index.isin(tickers)]
results.to_excel(f"{filter_folder}/good.xlsx", encoding="utf-8-sig")


'''filter_df["Indicator"] = filter_df.index.get_level_values(1)
print(filter_df.columns)'''

#
#results = results[results['Sàn'].isin(["HNX", "UPCoM"])]
#results.to_excel(f"{filter_folder}/good.xlsx", encoding="utf-8-sig")
#show_result(filter_df)










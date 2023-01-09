import os
import re
import pandas as pd
import time
import Support_function as Sf
import numpy as np
import requests as rq
from datetime import date, datetime
import math

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

main_folder = 'D:/Barn'


def get_root(main_folder_):
    root_path_ = main_folder_ + "/Root.csv"
    name = []
    file_path = []
    for _path, _subdirs, _files in os.walk(main_folder_):
        for _name in _files:
            _file_path = os.path.join(_path, _name).replace("\\", '/')
            name.append(re.sub(r'(\.).+', '', _name))
            file_path.append(_file_path)
    index = pd.Series(data=name, name='Ticker')
    df_ = pd.DataFrame(data=file_path, index=index, columns=['Path'])
    df_.to_csv(root_path_, encoding='utf-8-sig')
    return df_


class Database:
    def __init__(self, data_source):
        self.main_folder = main_folder
        self.root = root
        self.data_source = str(data_source).lower()
        self.database_path = self.main_folder + "/" + self.data_source + '_database.csv'
        Sf.backup(self.database_path)

    def data_purify(self, _df):
        _df = Sf.columns_clarify(_df)
        li = list(_df.columns)
        li = Sf.sort_columns(li)
        _df = _df.reindex(columns=li)
        return _df

    def get_file_path(self):
        container = self.data_source + "/"
        return self.root[self.root['Path'].str.contains(container)]

    def create(self):
        file_paths = self.get_file_path()
        dfs = []
        for i in range(len(file_paths)):
            df_ = pd.read_csv(file_paths.iloc[i, 0]).iloc[1:,:]
            df_.insert(0, "Ticker", file_paths.index[i], True)
            dfs.append(df_)
        df = pd.concat(dfs, axis=0)
        df.rename(columns={'Unnamed: 0': "Indicator"}, inplace=True)
        df = df.set_index(['Ticker', 'Indicator'])
        df = self.data_purify(df)
        df.to_csv(self.database_path, encoding='utf-8-sig')
        print(f"Done update market data")

    def update(self, _ticker):
        _ticker = _ticker.upper()
        _to_replace = pd.read_csv(root[root['Path'].str.contains(f"{_ticker}.csv")].iloc[0,0])
        _to_replace.insert(0, "Ticker", _ticker, True)
        _to_replace.rename(columns={'Unnamed: 0': "Indicator"}, inplace=True)
        _to_replace= _to_replace.set_index(['Ticker', 'Indicator'])
        _to_replace = self.data_purify(_to_replace)

        _database = pd.read_csv(self.database_path,index_col=[0,1]).drop(_ticker, level="Ticker")
        result = pd.concat([_database,_to_replace], axis=0)
        result.to_csv(self.database_path, encoding='utf-8-sig')
        print(f"Done update data for {_ticker}")


class DerivationDatabase:
    def __init__(self, data_source):
        self.main_folder = main_folder
        self.database_path = self.main_folder + "/" + data_source + '_database.csv'
        self.database = pd.read_csv(self.database_path, index_col=[0,1])
        self.derivation_path = self.database_path.replace('database', 'derivation')
        self.layout_path = self.main_folder + "/Layout.xlsx"
        self.derivation_index = pd.read_excel(self.layout_path,usecols=['name', 'look_up_name', 'industry']).set_index('name')
        self.main_industry = pd.read_csv(self.main_folder + '/General info.csv', encoding='utf-8-sig',
                                         usecols=[0, 2, 3, 4], index_col=0)
        Sf.backup(self.derivation_path)


    def get_derivative_param(self, separated_, item, indexes):
        def agr_cal(lk, df_):
            result_ = df_.xs(lk, level=1).iloc[0, :]
            try:
                if str(df_.columns[0]).startswith('Q'):
                    result_ = result_.reindex(index=result_.index[::-1]).diff(4)/result_.reindex(index=result_.index[::-1]).abs().shift(4)
                else:
                    result_ = result_.reindex(index=result_.index[::-1]).diff()/result_.reindex(index=result_.index[::-1]).abs().shift()

                return result_
            except IndexError:
                return None

        try:
            look_up_name = indexes.loc[item, 'look_up_name']
            if '/' in look_up_name and 'Chỉ số' not in look_up_name:
                sub = look_up_name.split("/")
                result = separated_.xs(sub[0], level=1).iloc[0, :] / separated_.xs(sub[1], level=1).iloc[0, :]
            elif 'AGR' in item:
                yearly_database = separated_[[i for i in separated_.columns if str(i).startswith('Y')]] \
                    .dropna(axis=1, how='all')
                quarterly_database = separated_[[i for i in separated_.columns if str(i).startswith('Q')]] \
                    .dropna(axis=1, how='all')
                result = pd.concat([agr_cal(look_up_name, yearly_database), agr_cal(look_up_name, quarterly_database)])
            elif 'RO' in item:
                result = separated_.xs(look_up_name, level=1).iloc[0, :] / 100
            elif 'P/E' in item:
                try:
                    base_price = separated_.xs('Chỉ số giá thị trường trên giá trị sổ sách (P/B)', level=1).iloc[0, :] * \
                                 separated_.xs('Giá trị sổ sách của cổ phiếu (BVPS)', level=1).iloc[0, :]
                    result = round(base_price / separated_.xs('Thu nhập trên mỗi cổ phần của 4 quý gần nhất (EPS)',
                                                        level=1).iloc[0, :],2)
                except KeyError:
                    result = round(separated_.xs(look_up_name, level=1).iloc[0, :],2)
            else:
                result = separated_.xs(look_up_name, level=1).iloc[0, :]
        except KeyError:
            result = np.empty(shape=len(separated_.columns))
        return pd.Series(result, name=item).replace([r'0\.0*$', 0], np.nan)

    def rename_index(self,df):
        new_name_ = ['Doanh thu thuần', 'Lợi nhuận gộp', 'Lợi nhuận sau thuế']
        for name_ in new_name_:
            for i in range(len(df.index)):
                if str(df.index.get_level_values(1)[i]).startswith(name_):
                    old = df.index.get_level_values(1)[i]
                    df = df.rename(index={old: name_})
                    break
                else:
                    continue

        return df

    def get_single_derivation(self, ticker_):
        separated_ = self.database[self.database.index.get_level_values(0) == ticker_]

        #Unify the name of fiscal indices
        separated_ = self.rename_index(separated_)

        temp_ = pd.DataFrame()#columns=separated_.columns
        try:
            bank = self.main_industry.loc[ticker_, 'Ngành cấp 2']
            if bank == 'Trung gian tín dụng và các hoạt động liên quan':
                indexes = self.derivation_index[self.derivation_index['industry'].isin(
                    ['Trung gian tín dụng và các hoạt động liên quan', 'Toàn bộ'])]
            else:
                indexes = self.derivation_index[self.derivation_index['industry'].isin(['Khác', 'Toàn bộ'])]
        except KeyError:
            indexes = self.derivation_index[self.derivation_index['industry'].isin(['Khác', 'Toàn bộ'])]

        for item in indexes.index:
            temp_ = pd.concat([temp_,pd.DataFrame(self.get_derivative_param(separated_, item, indexes)).transpose()],axis=0)
        idx0 = [ticker_.upper() for i in range(len(temp_.index))]
        temp_ = temp_.set_index([idx0, temp_.index])
        return temp_

    def create_derivation(self):
        result = pd.DataFrame()
        tickers = self.database.index.get_level_values(0).drop_duplicates()
        for ticker in tickers:
            if len(ticker) == 3:
                try:
                    temp_ = self.get_single_derivation(ticker)
                    result = pd.concat([result,temp_])
                except KeyError as e:
                    print("Error when calculating " + str(e) + " at ticker: " + str(ticker))
            else:
                continue
        result.index.names = ['Ticker', 'Indicator']
        result.dropna(axis=1,how="all")
        result.to_csv(self.derivation_path, encoding='utf-8-sig')
        print(f"Done update market derivation data")

    def update(self,_ticker):
        _ticker = _ticker.upper()
        _separated_database = self.database[self.database.index.get_level_values(0) == _ticker]
        temp_ = self.get_single_derivation(_ticker)
        _derivation_database = pd.read_csv(self.derivation_path, index_col=[0, 1]).drop(_ticker, level="Ticker")
        result = pd.concat([_derivation_database, temp_], axis=0)
        result.to_csv(self.derivation_path, encoding='utf-8-sig')
        print(f"Done update data for {_ticker}")

root = get_root(main_folder)

'''start = time.time()
database = Database('vietstock')
database.create()
print(time.time()-start)

start = time.time()
new_derivation = DerivationDatabase('vietstock')
new_derivation.create_derivation()
print(time.time()-start)'''
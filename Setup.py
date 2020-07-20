import os
import re
import pandas as pd
import time
from Layout import traces
import Support_function as Sf
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''IDEA
- Append and merge all month, year, source to one single file
- Add source col
'''
'''
INSERT SOURCE COL, SORT GROUP OF COLUMNS NAME AND UNITED COLUMNS NAME
'''

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def get_root(_directory, root_path_):
    name = []
    file_path = []
    for _path, _subdirs, _files in os.walk(_directory):
        for _name in _files:
            _file_path = os.path.join(_path, _name).replace("\\", '/')
            name.append(re.sub(r'(\.).+','',_name))
            file_path.append(_file_path)
    df_ = pd.DataFrame(data = file_path, index = name).to_csv(root_path_, index_label=['Ticker'], header=['Path'], encoding='utf-8-sig')
    return df_


def get_range_in_root(root_df, string):
    num = len(root_df.index)
    print(num)
    start = 0
    stop = 0
    for i in range(0, num, 1):
        if string in root_df.iloc[i,0] and len(root_df.index[i]) == 3:
            start = i
            break
    for j in range(num-1,-1,-1):
        if string in root_df.iloc[j,0] and len(root_df.index[j]) == 3:
            stop = j
            break
    return [start, stop+1]


def all_to_one(database_path_, source):
    total = pd.DataFrame()
    data_range = get_range_in_root(root,source)
    print(data_range)
    for i in range(data_range[0], data_range[1]):
        ticker = root.index[i]
        path = root.iloc[i, 0]
        df_ = pd.read_csv(path)
        if df_.iloc[0, 0] == ticker: #cophieu68 with 3 unnamed col
            df_.rename(columns={'Unnamed: 0': "Ticker", 'Unnamed: 2': "Indicator"}, inplace=True)
            df_ = df_.drop(columns='Unnamed: 1', axis=1)
        else:
            df_.insert(0, "Ticker", [ticker for i in range(df_.shape[0])], True)
            df_.rename(columns={'Unnamed: 0': "Indicator"}, inplace=True)
        total = total.append(df_)
        print(i)
    print(total.columns)
    total.to_csv(database_path_, encoding='utf-8-sig')



def data_purify(file_path_):
    cols = pd.read_csv(file_path_, nrows=1).columns
    df2 = pd.read_csv(file_path_, thousands=',', dtype='unicode', usecols=cols[1:])
    Sf.to_float64(df2)
    df2 = Sf.remove_invalid_columns(df2)
    li = list(df2.columns)
    li = Sf.sort_columns(li)
    df2 = df2.reindex(columns=li)
    df2 = Sf.rename_column(df2)
    df2.to_csv(file_path_, encoding='utf-8-sig')
    return df2


def run_crawl_general_info(directory):
    driver = webdriver.Chrome()
    url = 'https://finance.vietstock.vn/doanh-nghiep-a-z/danh-sach-niem-yet?page=1'
    driver.get(url)
    pages = int(driver.find_element_by_xpath('//*[@id="az-container"]/div[1]/div[2]/div/span[1]/span[2]').text)

    col_element = driver.find_elements_by_xpath('//*[@id="az-container"]/div[2]/table/thead/tr/th')
    column = [col.text for col in col_element]
    table = []

    for page in range(1, pages+1):
        time.sleep(3)
        rows = driver.find_elements_by_xpath('//*[@id="az-container"]/div[2]/table/tbody/tr')
        for row in rows:
            cells = row.find_elements_by_tag_name('td')
            row_data = [cell.text for cell in cells[1:]]
            table.append(row_data)
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-page-next"]'))).click()
        except exceptions.TimeoutException:
            print('Next button: disable')

    df = pd.DataFrame(table, columns=column[1:])
    df.to_csv(root.loc['General info', 'Path'], encoding="utf-8-sig")
    driver.quit()


main_folder = 'D:/Barn'
root_path = main_folder+"/Root.csv"
get_root(main_folder, root_path)
root = pd.read_csv(root_path, index_col=0)



'''range = get_range_in_root(root,'cophieu68')
source = pd.DataFrame(root.iloc[range[0]:range[1]])

annual_range = get_range_in_root(source, 'Annual')
annual = pd.DataFrame(source.iloc[annual_range[0]:annual_range[1]])
print(annual)'''

'''
#vs_path ='D:/Barn/vietstock_database.csv'
data_path = root.loc['cophieu68_database', 'Path']
#data_purify(data_path)
cols = list(pd.read_csv(data_path, nrows =1))
df = pd.read_csv(data_path, index_col=['Ticker','Indicator'], usecols=[i for i in cols if i!= 'Unnamed: 0'])
quater_database = df.filter(regex='^Q').dropna(how='all', axis=0).dropna(how='all',axis=1)
print(quater_database.columns)
'''


def get_derivation(database):
    result = pd.DataFrame()
    list_ = database.index.get_level_values(0).drop_duplicates()
    for i in list_:
        try:
            df = database[database.index.get_level_values(0) == i]
            temp_ = Sf.get_data(i, df, traces)
            result = result.append(temp_)
        except KeyError as e:
            print("Error when calculating " + str(e)+ " at ticker: "+str(i))
    result.index.names = ['Ticker', 'Indicator']
    return result


def create_derivation_csv(database_name):
    data_path = root.loc[database_name, 'Path']
    cols = list(pd.read_csv(data_path, nrows=1))
    df_ = pd.read_csv(data_path, index_col=['Ticker', 'Indicator'], usecols=[i for i in cols if i != 'Unnamed: 0'])
    quarter_database = df_.filter(regex='^Q').dropna(how='all', axis=0).dropna(how='all', axis=1)
    annual_database = df_.filter(regex='^Y').dropna(how='all', axis=0).dropna(how='all', axis=1)
    derivation_quarter = get_derivation(quarter_database)
    derivation_annual = get_derivation(annual_database)
    result = pd.concat([derivation_annual, derivation_quarter], axis=1, sort=False)
    result_path = str(data_path).replace('database','derivation')
    result.to_csv(result_path, encoding="utf-8-sig")
    return result

#print(create_derivation_csv('cophieu68_database'))
'''data_path = root.loc['cophieu68_database', 'Path']
cols = list(pd.read_csv(data_path, nrows=1))
df_ = pd.read_csv(data_path, index_col=['Ticker', 'Indicator'], usecols=[i for i in cols if i != 'Unnamed: 0'])
quarter_database = df_.filter(regex='^Q').dropna(how='all', axis=0).dropna(how='all', axis=1)
df = quarter_database[quarter_database.index.get_level_values(0)=='AAA']
temp_ = Sf.get_data('AAA', df, traces)
print(temp_)'''































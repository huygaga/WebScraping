from bs4 import BeautifulSoup
import datetime
import re
import getpass
import openpyxl as xl
import requests
from lxml.html import fromstring
import time
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import colorsys
import plotly.graph_objects as go


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Replace error expression in string:
def clarify(text):
    error_char = [u'\xa0', ',','N/A']
    replace_char = [u' ', '','NaN']
    '''
        error_char = [u'\xa0', ',', 'N/A', "Q1 ", "Q2 ", "Q3 ", "Q4 "]#'Kết Quả Kinh Doanh'
    replace_char = [u' ', '', '=NA()', "03/30/", "06/30/", "09/30/", "12/30/"]#'Thời gian'
    '''
    text = text.strip()
    for i in range(len(error_char)):
        try:
            if error_char[i] in text:
                text = text.replace(error_char[i], replace_char[i])
        except TypeError:
            text = re.sub(error_char[i], replace_char, text)

    # Remove "(EPS chua dieu chinh)" 'cause unable finding a way to append additional col for it
    # SOLVE IT LATER
    text = re.sub(" \(.*\)", "", text)
    return text


# Avoid error while writing excel file (as the data format is string)
def safe_format(value):
    if is_valid_date(value):
        value = datetime.datetime.strptime(value, "%m/%d/%Y").date()
    else:
        try:
            value = float(value)
        except ValueError:
            pass
    return value


# Check if entire row was empty:
def is_empty(row):
    bol = True
    for cell in row:
        try:
            if cell.get_text():
                bol = False
        except AttributeError:
            pass
    return bol


# Check validation of date value:
def is_valid_date(str):
    try:
        month, day, year = str.split('/')
        valid = True
    except ValueError:
        valid = False
    return valid


def convert_vndate_to_standard(str):
    try:
        day, month, year = str.split('/')
        return '{}/{}/{}'.format(month, day, year)
    except ValueError:
        return None


def create_wb(file_name):
    wb = xl.Workbook()
    folder = 'C:/Users/' + getpass.getuser() + '/Desktop/New Folder/'
    s_path = folder + file_name + ' ' + datetime.datetime.now().strftime("%d-%m-%d_%H.%M.%S") + '.xlsx'
    wb.save(s_path)
    return s_path


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def close_start_popup(driver):
    try:
        main_window_handle = None
        while not main_window_handle:
            main_window_handle = driver.current_window_handle
        pop_up_class = ['closeBtn', 'skylight-close-button']
        for pop in pop_up_class:
            driver.find_element_by_class_name(pop).click()
        driver.switch_to.default_content()
        time.sleep(10)
    except exceptions.NoSuchElementException:
        None


'''
USE FOR DYNAMIC WEBPAGE AND REQUIRING FOR CLICK NEXT/ PREVIOUS TO DISPLAY CONTINUOUS DATA 
'''



def get_page_webdriver(url_):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url_)
    WebDriverWait(driver, 20).until(lambda x: x.find_element_by_tag_name('tr'))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(2)
    driver.quit()
    return soup

def rename_files_inside_container(container_path, old_name, new_name):
    import os
    path = container_path
    files = os.listdir(path)
    for index, file in enumerate(files):
        os.rename(os.path.join(path, file), os.path.join(path,file.replace(old_name, new_name)))

def get_column_header_from_file(_directory, col_no):
    try:
        _df = pd.read_csv(_directory, index_col=0)
        return _df.columns[col_no]
    except (FileNotFoundError, IndexError):
        return None


def get_column_data_from_file(_directory, col_no, _dtype=np.unicode_):
    _df = pd.read_csv(_directory, index_col=0)
    return np.array(_df.iloc[:, col_no], dtype=_dtype)


def growth_rate(df_, look_back=4):
    df_ = df_.reindex(index=df_.index[::-1]).pct_change(periods=look_back)
    df_ = df_.reindex(index=df_.index[::-1])
    return df_


def get_df_row_data(_df,_str):
    return _df.xs(_str, level=1).iloc[0, :]


def trace_data(dict_, x, y):
    if str(dict_['type']).lower() == 'bar':
        return go.Bar(x=x, y=y, name=dict_['name'], opacity=0.5, marker=dict_['marker color'])
    else:
        return go.Scatter(x=x, y=y, mode='lines', name=dict_['name'], marker=dict_['marker color'])

def get_derivative_param(df_, dict_):
    if '/' in dict_['look_up_name']:
        sub = dict_['look_up_name'].split("/")
        plot = get_df_row_data(df_, sub[0])/get_df_row_data(df_, sub[1])
    elif 'AGR' in dict_['name']:
        plot = get_df_row_data(df_, dict_['look_up_name'])
        if str(df_.columns[0]).startswith('Q'):
            plot = growth_rate(plot)
        else:
            plot = growth_rate(plot, 1)
    else:
        plot = get_df_row_data(df_, dict_['look_up_name'])
    return plot


def get_data(ticker_, df_, traces_dict_):
    temp_ = pd.DataFrame(columns=df_.columns)
    for key in traces_dict_.keys():
        temp_ = temp_.append(pd.Series(get_derivative_param(df_, traces_dict_[key]), name=traces_dict_[key]['name']))
    idx0 = [ticker_.upper() for i in range(len(temp_.index))]
    temp_ = temp_.set_index([idx0, temp_.index])
    return temp_



def lighten_darken_color(color, factor):
    color = color.replace('rgb(', '').replace(')', '').split(',')
    color = [int(col) / 255.0 for col in color]
    color = colorsys.rgb_to_hls(color[0], color[1], color[2])
    color = colorsys.hls_to_rgb(color[0], color[1] * factor, color[2])
    color = [int(col * 255) for col in color]
    return 'rgb({},{},{})'.format(color[0],color[1],color[2])


def marker_control(color):
    return {'color': color,
            'line_color': lighten_darken_color(color,0.5)
            }

def is_nan(num):
    return num != num

def axis_limit(_list, coverage=1):
    # Coverage = 1 mean axis range won't cover the largest and smallest value
    min = max = 0
    non_nan = [i for i in _list if not is_nan(i)]
    if np.sort(non_nan)[-coverage] > max:
        max = np.sort(non_nan)[-coverage]
    if np.sort(non_nan)[coverage-1] < min:
        min = np.sort(non_nan)[coverage-1]
    return min, max

def get_page(url_):
    # APPLYING FOR STATIC PAGE
    """ Avoid blocking by:
    1- Pretent to be genuine users
    2- Crawling slowly (interval random.between 1-15s)
    3- Rotating IP address NOT YET WORK"""

    time.sleep(random.randrange(3, 10, 1))
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                             'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
               'Accept': 'text/html,application/xhtml+xml,application/xml;'
                         'q=0.9,image/webp,*/*;q=0.8'}
    try:
        rq = session.get(url_, headers=headers)
        encoding = rq.encoding if 'charset' in rq.headers.get('content-type', '').lower() else None
    except requests.exceptions.RequestException:
        return None
    return BeautifulSoup(rq.content, 'html.parser', from_encoding=encoding)




'''def get_title(ticker):
    ticker_info = list(pd.read_csv(root.loc['General info', 'Path'], index_col=1).loc[ticker, :])
    dict_ = {}
    dict_['full_name'] = ticker_info[1]
    dict_['industry_1'] = ticker_info[2]
    dict_['industry_2'] = ticker_info[3]
    dict_['industry_3'] = ticker_info[4]
    dict_['market'] = ticker_info[5]
    dict_['ngay_GDDT'] = ticker_info[6]
    dict_['Khoi luong NY/DKGD'] =ticker_info[7]
    return dict_'''




'''def is_empty_ticker(ticker):
    try:
        return ticker not in root.index or pd.read_csv(root.loc[ticker, 'Path'], index_col=[0, 1, 2]).empty
    except KeyError:
        return True'''


def shift_to_top(list_,ticker_):
    list_.remove(ticker_)
    list_.insert(0, ticker_)
    return list_


def timer(func):
    start_time = time.time()
    func()
    return("--- %s seconds ---" % (time.time() - start_time))

'''def fix_lower_case_index_error(ticker_):
    df_ = pd.read_csv(root.loc[ticker_,'Path'],index_col=0)
    df_.index  = df_.index.str.upper()
    df_.to_csv(root.loc[ticker_,'Path'],encoding='utf-8-sig')
    return df_'''


# DATAFRAME RESHAPE FUNCTION
def sort_quarterly(li):
    yearly_re = '([0-9]{4})'
    quarterly_re = '([1-4]{1}?)'

    natural_sort(li, yearly_re)
    years = [re.search(yearly_re,key).group() for key in li]
    years = list(dict.fromkeys(years))
    result = []
    for year in years:
        temp = [i for i in li if year in i]
        natural_sort(temp, quarterly_re)
        for t in temp:
            result.append(t)
    return result


def sort_yearly(li):
    yearly_re = '([0-9]{4})'
    natural_sort(li, yearly_re)
    return li


def natural_sort(_list, reg, reverse=True): # Sort list of number-included-string
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.search(reg,key).group()]
    _list.sort(key=alphanum_key)
    if reverse:
        _list.reverse()
    return _list


def sort_columns(list):
    yearly_re = '([0-9]{4})'
    title = []
    year = []
    quarter = []
    for i in list:
        if re.search('^[Qq]',str(i)):
            quarter.append(i)
        elif re.search(yearly_re,str(i)):
            year.append(i)
        else: title.append(i)
    year = sort_yearly(year)
    quarter = sort_quarterly(quarter)
    result = []
    for i in title:
        result.append(i)
    for i in year:
        result.append(i)
    for i in quarter:
        result.append(i)
    return result


def to_float64(df_):
    for col in df_.columns:
        try:
            df_[col] = df_[col].str.replace(',', '').replace('-', 0)
            df_[col] = df_[col].astype('float64')
        except ValueError:
            print('Unable converting '+ col+ ' column to float64')
            continue
    return df_


def remove_invalid_columns(df_):
    df_ = df_.loc[:, ~df_.columns.str.replace("(\.\d+)$", "").duplicated()]
    df_ = df_.dropna(how='all', axis=1)
    for col in df_.columns:
        if col.isdigit() and int(col)<2000:
            print(col)
            df_ = df_.drop(col, axis =1)
    return df_


def rename_column(df_):
    name = [(col, "Y"+str(col)) for col in df_.columns if str(col).isdigit()]
    df_.rename(columns= dict(name), inplace=True)
    return df_
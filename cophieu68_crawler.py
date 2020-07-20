from bs4 import BeautifulSoup
import requests
import Support_function as Sf
import time
import random
import pandas as pd
import re
from datetime import datetime
import numpy as np
import os
from Setup import root


# TO DISPLAY OUTPUT DATAFRAME:
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

barn_path = 'D:/Barn/Financial data/cophieu68/'

class Website:
    def __init__(self, _ticker, assess_period= "Quarter"):
        self.index = 'https://www.cophieu68.vn/'
        self._ticker = _ticker
        self.assess_period = assess_period
        self.view_period = 0 if assess_period == 'Quarter' else -1

        self.reports = {
            # Name of report : [ Nav_chars, heading_1 tag, heading_2 tag, data_tag]
            'Bao cao tai chinh': [self.get_url('ist'), 'td[colspan="2"]', 'td:nth-of-type(2)', 'td[align=right]'],
            'Can doi ke toan': [self.get_url('bs'), 'td[colspan="2"]', 'td:nth-of-type(2)', 'td[align=right]'],
            'Luu chuyen tien te': [self.get_url('cf'), 'td:nth-of-type(1)[style="width:5px"]~td', 'td:nth-of-type(2)[align!=right]', 'td[align=right]:not([style])']
        }
        print(self._ticker, end='')
        print(self.reports)

    def get_url(self, nav_chars):
        url = '{}{}{}{}{}{}{}'.format(self.index, 'incomestatement.php?id=', self._ticker, '&view=', nav_chars,
                                      '&year=', self.view_period)
        return url


class Crawler:
    def __init__(self, site):
        self.reports = site.reports
        self._ticker = site._ticker
        self.period = site.assess_period
        self.columns_header =[]
        self.result = pd.DataFrame()
        self.file_path = barn_path+self.period+"/"+str(self._ticker)+'.csv'

    def check_last_update(self):
        try:
            return pd.read_csv(self.file_path, index_col=[0, 1, 2]).columns[0]
        except IndexError:
            return ''

    def sort_columns_header(self):
        self.columns_header = list(dict.fromkeys(self.columns_header))
        self.columns_header.sort(key=lambda day: datetime.strptime(day, "%m/%d/%Y"))
    
    def get_trow_data(self, selector, trow):
        data = []
        for cell in trow.select(selector, recursive=False):
            text_ = Sf.clarify(cell.text)
            data.append(text_)
            if Sf.is_valid_date(text_):
                self.columns_header.append(text_)
        return data

    def get_trow_heading(self, h_, trow):
        try:
            header = Sf.clarify(trow.select_one(h_).text)
            header = re.sub('^-', "", header) # put it in Sf.Clarify later
        except AttributeError:
            return ''
        return header

    def crawl(self):
        for key, item in self.reports.items():
            url_ = item[0]
            h1 = item[1]
            h2 = item[2]
            data_tag = item[3]
            soup = Sf.get_page_webdriver(url_)
            table = soup.find('table')
            header_0 = []
            header_1 = []
            header_2 = []
            data = []

            report_name = Sf.clarify(table.select_one('tr.tr_header > td:nth-child(1)').text)
            for trow in table.find_all('tr'):
                if Sf.is_empty(trow):
                    continue
                else:
                    dat = self.get_trow_data(data_tag, trow)
                    h_1 = self.get_trow_heading(h1, trow)
                    if h_1 is not None and len(h_1) > 0:
                        h_2 = h_1
                    elif trow.get('class') == ['tr_header']:
                        h_1 = h_2 = report_name
                    else:
                        h_1 = header_1[-1]
                        h_2 = self.get_trow_heading(h2, trow)
                    header_0.append(self._ticker)
                    header_1.append(h_1)
                    header_2.append(h_2)
                    data.append(dat)

            header_0[0] = 'Index 1'
            header_1[0] = 'Index 2'
            header_2[0] = 'Index 3'
            df = pd.DataFrame(data, index=[header_0, header_1, header_2])
            new_header = df.iloc[0]
            df = df[1:]
            df.columns = new_header
            self.result = self.result.append(df)

        if self.result.empty:
            pass
        else:
            self.result.to_csv(self.file_path, encoding='utf-8-sig')
            print("Success")


def run_crawl(tickers_list_):
    for ticker_ in tickers_list_:
        site = Website(ticker_,'Annual')
        try:
            Crawler(site).crawl()
        except:
            print('Error crawling: '+ticker_)


tickers = list(root.index[~(root.index.str.len()!=3)])
#run_crawl(tickers)

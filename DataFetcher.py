import requests as rq
import time
import json
import random
import pandas as pd
from BarnStructure import root, main_folder, Database, DerivationDatabase
import Support_function as Sf
import os
from datetime import date, datetime, timedelta
import win32com.client, time
import re
from googlesearch import search
import math
from bs4 import BeautifulSoup
import json
import codecs
from dateutil.relativedelta import relativedelta

'''
# GET HISTORICAL TRADING DATA INCLUDING FOREIGN...:
URL: https://finance.vietstock.vn/VNM/thong-ke-giao-dich.htm?grid=market
XHR: gettradingresult
'''
'''
    MUST MANUALLY LOGIN TO SITE AND GET NEW COOKIES, SO TIRED TO TRY AUTO LOGIN USING OAUTH2 
    COPY > Copy all as cURL (bash)
    Then paste to https://curl.trillworks.com/ to get python request
'''

# VIETSTOCK PARAMS:
separated_datafiles_container = f'{main_folder}/Financial data/vietstock'

#Below RequestVerificationToken is for payload, different from one for cookies
RequestVerificationToken = 'tqN_bO3Nyaw6iMrTLTfpXy642sjjNyTE8S7LYFwZRp4DxL_5f63VIPrjfaBq8wSxz6PQZlNosWDbP1uszdXAlcyFSasO-QKCoKx_xAasLJpgyTIu4AZ6RXSxzorUnVmM0'
cookies = {
    'language': 'vi-VN',
    'Theme': 'Light',
    'AnonymousNotification': '',
    '_pbjs_userid_consent_data': '3524755945110770',
    '_ga': 'GA1.2.548537052.1656643483',
    'dable_uid': '50924091.1656643483306',
    '_cc_id': 'efe2b7639633884c7ecc1b6bc916ff7e',
    'cto_bundle': '0WSsK19RR2x1TkhqRGZPOHEzVGJwRWlITzZGN3hrc2NmJTJGVEdMZnM4RUFmc0dNJTJCQ0dJd2N4OEFndWdjMXhzR1F0MkJoYWFkY0xnZyUyQnJNSXBZUlY0anRHNyUyRkp3Zm40dXBhOWxMd1hySGhKQmd4MG1McmxQWjM3ZjFnUWloVUtWTVZvUmh2UTh6OElpaHlhQ2IlMkJPJTJGciUyRkRCJTJCMExnJTNEJTNE',
    'dable_uid': '50924091.1656643483306',
    '_gac_UA-1460625-2': '1.1657365524.Cj0KCQjwzqSWBhDPARIsAK38LY_8azZAQxs53nmFxh1raW3hC-tB4K4dJrWfxWAmg5gCKxV2YkhFYSkaAslPEALw_wcB',
    '_gac_UA-166274536-7': '1.1657365526.Cj0KCQjwzqSWBhDPARIsAK38LY_8azZAQxs53nmFxh1raW3hC-tB4K4dJrWfxWAmg5gCKxV2YkhFYSkaAslPEALw_wcB',
    '_gid': 'GA1.2.857294522.1657500233',
    '__gpi': 'UID=0000073d4006b9b6:T=1656643482:RT=1657500226:S=ALNI_Mbw74lYOV0Yp4RH_5_KlKm_lvfu9A',
    'vts_usr_lg': 'AB6643FABAB51D2C35F22FAE9A3A96CB0992DF02E0B2A2A6767B07EF4F852F6886D62CDB6EA4A78921FEC62B1D35D64575CB1B0B0D864C92B7AB790B65328D039948B452226A24A3ECFC7BF9C742AA7309ED3E194C04B78F382FD073A9881F3283785F066208E14FD300148DBF61DEAC6AAE2FE344BBEA5DA3E1169E8B5E4F30',
    'ASP.NET_SessionId': 'rezhol00czusx2rcnthalhsi',
    '__RequestVerificationToken': 'qWyY7X-ZXS1_x5cRwUWA-p5LfI_EAmaDYohKhTE75GTvJ32JNhYz-huR61N_z1Q8iBwJaUeGN84aFRRxhke1SIyMZF-eaA5phVWZyGaC_7s1',
    '_gat_gtag_UA_1460625_2': '1',
    '_gat_UA-1460625-2': '1',
    '__gads': 'ID=d02427d639fd9740:T=1656643482:S=ALNI_MZ8SZpzs2fKqwO1FmVBxpwgyRSiIg',
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'language=vi-VN; Theme=Light; AnonymousNotification=; _pbjs_userid_consent_data=3524755945110770; _ga=GA1.2.548537052.1656643483; dable_uid=50924091.1656643483306; _cc_id=efe2b7639633884c7ecc1b6bc916ff7e; cto_bundle=0WSsK19RR2x1TkhqRGZPOHEzVGJwRWlITzZGN3hrc2NmJTJGVEdMZnM4RUFmc0dNJTJCQ0dJd2N4OEFndWdjMXhzR1F0MkJoYWFkY0xnZyUyQnJNSXBZUlY0anRHNyUyRkp3Zm40dXBhOWxMd1hySGhKQmd4MG1McmxQWjM3ZjFnUWloVUtWTVZvUmh2UTh6OElpaHlhQ2IlMkJPJTJGciUyRkRCJTJCMExnJTNEJTNE; dable_uid=50924091.1656643483306; _gac_UA-1460625-2=1.1657365524.Cj0KCQjwzqSWBhDPARIsAK38LY_8azZAQxs53nmFxh1raW3hC-tB4K4dJrWfxWAmg5gCKxV2YkhFYSkaAslPEALw_wcB; _gac_UA-166274536-7=1.1657365526.Cj0KCQjwzqSWBhDPARIsAK38LY_8azZAQxs53nmFxh1raW3hC-tB4K4dJrWfxWAmg5gCKxV2YkhFYSkaAslPEALw_wcB; _gid=GA1.2.857294522.1657500233; __gpi=UID=0000073d4006b9b6:T=1656643482:RT=1657500226:S=ALNI_Mbw74lYOV0Yp4RH_5_KlKm_lvfu9A; vts_usr_lg=AB6643FABAB51D2C35F22FAE9A3A96CB0992DF02E0B2A2A6767B07EF4F852F6886D62CDB6EA4A78921FEC62B1D35D64575CB1B0B0D864C92B7AB790B65328D039948B452226A24A3ECFC7BF9C742AA7309ED3E194C04B78F382FD073A9881F3283785F066208E14FD300148DBF61DEAC6AAE2FE344BBEA5DA3E1169E8B5E4F30; ASP.NET_SessionId=rezhol00czusx2rcnthalhsi; __RequestVerificationToken=qWyY7X-ZXS1_x5cRwUWA-p5LfI_EAmaDYohKhTE75GTvJ32JNhYz-huR61N_z1Q8iBwJaUeGN84aFRRxhke1SIyMZF-eaA5phVWZyGaC_7s1; _gat_gtag_UA_1460625_2=1; _gat_UA-1460625-2=1; __gads=ID=d02427d639fd9740:T=1656643482:S=ALNI_MZ8SZpzs2fKqwO1FmVBxpwgyRSiIg',
    'Referer': 'https://finance.vietstock.vn/doanh-nghiep-a-z/?page=1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_general_info():
    def parse_time(string):
        try:
            time_stamp = int(re.findall(r'\d+', string)[0]) / 1000
            date = datetime.fromtimestamp(time_stamp).strftime('%d/%m/%Y')
            return date
        except TypeError:
            return ''

    url = 'https://finance.vietstock.vn/data/corporateaz'
    payload = {
        'catID': '0',
        'industryID': '0',
        'page': 1,
        'pageSize': '20',
        'type': '1',
        'code': '',
        'businessTypeID': '0',
        'orderBy': 'Code',
        'orderDir': 'ASC',
        '__RequestVerificationToken': RequestVerificationToken
    }
    path_ = root.loc['General info', 'Path']
    Sf.backup(path_)
    columns = pd.read_csv(path_, index_col=0).columns
    df = pd.DataFrame()

    result = rq.post(url, data=payload, headers=headers, cookies=cookies).json()
    total_pages = math.ceil(int(result[0]['TotalRecord']) / 20)  # 'cos 20 items/page
    while payload['page'] <= total_pages:
        print('Getting data page ' + str(payload['page']))
        result = rq.post(url, data=payload, headers=headers, cookies=cookies).json()
        for row in result:
            date = parse_time(row['FirstTradeDate'])
            ser = pd.Series(
                data=[row['Name'],
                      row['IndustryName1'],
                      row['IndustryName2'],
                      row['IndustryName3'],
                      row['Exchange'],
                      date,
                      row['TotalShares'],
                      ], name=row['Code'])
            df = df.append(ser)
        payload['page'] += 1
    df.columns = columns
    df.index.name = 'Ticker'
    df.to_csv(path_, encoding="utf-8-sig")
    print('Done crawling General info')


class Dividend:
    def __init__(self):
        self.request_url = "https://finance.vietstock.vn/data/eventstypedata"
        self.payload = {
            "eventTypeID": 1,
            "channelID": 0,
            "catID": -1,
            "page": 1,
            "pageSize": 50,
            "orderBy": "Date1",
            "orderDir": "DESC",
            '__RequestVerificationToken': RequestVerificationToken
        }
        self.file_path = f'{main_folder}/temp_/dividend.csv'

    def get_single_page(self, __post_date):
        result = rq.post(self.request_url, data=__post_date, headers=headers, cookies=cookies).json()
        _temp = pd.DataFrame.from_dict(result[0], orient="columns")
        print(_temp.head(10))
        return _temp

    def get_all_pages(self):
        __df = pd.DataFrame()
        __payload = self.payload
        while True:
            try:
                _temp = self.get_single_page(__payload)
                __df = pd.concat([__df, _temp])
            except ValueError:
                break
            __payload['page'] += 1
        return __df

    def data_cleaner(self, _df):
        def parse_time(__df):
            for c in __df.columns:
                if any(sub in c for sub in ["Date", "Time"]):
                    extracted = __df[c].str.extract(r"(\d+)")
                    __df[c] = extracted
                    parsed = __df[c].apply(lambda x: datetime.fromtimestamp(float(x) / 1000) if pd.notnull(x) else x)
                    __df[c] = parsed
            return __df

        using_col = ['Code', 'GDKHQDate', 'Note', 'Name']
        _df = _df[using_col]
        _df = parse_time(_df)
        return _df

    def run(self):
        __df = self.get_all_pages()
        __df = self.data_cleaner(__df)
        __df.to_csv(self.file_path, encoding='utf-8-sig')
        print("Done")
        return __df





# UPDATE FOR SINGLE TICKER
class DataUpdater:
    def __init__(self, ticker_):
        self.ticker = ticker_
        self.data_source = 'vietstock'
        self.file_path = self.get_file_path()

    def get_file_path(self):
        folder = root[root['Path'].str.contains(self.data_source)]
        file_path = folder.loc[self.ticker, 'Path']
        return file_path

    def update_financial_data_from_web(self, term_):
        try:
            new_data = FinancialCrawler(self.ticker, term_)
            payload_ = new_data.payload
            df_ = new_data.get_single_page(payload_)
            print(f"Done getting {term_} data for: {self.ticker}.")
            return df_
        except:
            print(f'Error at ticker: {self.ticker}.')

    def update(self):
        Sf.backup(self.file_path)
        old_data = pd.read_csv(self.file_path, index_col=0)
        term_ = ['annual', 'quarterly']
        for t in term_:
            df_ = self.update_financial_data_from_web(t)
            print(df_)
            try:
                for c in df_.columns:
                    # CHECK CURRENT DATA AND UPDATE NEW DATA IF ANY
                    try:
                        if df_[c].equals(old_data[c]):
                            continue
                        else:
                            print(f'Miss matching data at {c}')
                            old_data[c] = df_[c]
                            print(f'Replaced {c} column')
                    except KeyError as e:  # Mean new column occur
                        print(f'Add new column: {e}')
                        first_ = str(c)[0]
                        order_ = list(old_data.columns)
                        for i in range(len(order_)):
                            if str(order_[i]).startswith(first_):
                                old_data.insert(i, c, df_[c])
                                break
            except AttributeError:
                continue
        old_data.to_csv(self.file_path, encoding='utf-8-sig')
        print(f'Done {self.ticker}')




class AmibrokerFetch:
    def __init__(self):
        self.path_ = f'{main_folder}/temp_/live_data.csv'
        self.apx_path = f"{main_folder}/getBasicDataFromAmibroker.apx"

    def is_updated(self):
        try:
            mtime = os.path.getmtime(self.path_)
        except FileNotFoundError:
            return False

        today = date.today()
        last_modify = date.fromtimestamp(mtime)
        if (last_modify == today) or (today.weekday() in [5, 6]):
            return True
        else:
            return False

    def fetcher(self):
        """This will get new data of price, average trading value of the stock"""
        ab = win32com.client.Dispatch("Broker.Application")
        ab.Visible = True
        try:
            new_analysis = ab.AnalysisDocs.Open(self.apx_path)
            if new_analysis:
                new_analysis.Run(1)
                while new_analysis.IsBusy:
                    time.sleep(3)
                export = new_analysis.Export(self.path_)
                new_analysis.Close()
                print('AmiBroker Analysis Export result {}'.format(export))
        except Exception as e:
            print("AmiBroker EXCEPTION:")
            print(e)
        ab.Quit()
        return None

    def data_cleaner(self):
        df = pd.read_csv(self.path_, index_col=['Ticker']).drop("Date/Time", axis=1)
        df['Value'] = df['Value'] / 1000
        return df

    def run(self):
        if self.is_updated():
            print("Daily data updated")
        else:
            self.fetcher()
            print(f"Run updater on {date.today()}")
        df = self.data_cleaner()
        return df


# UPDATE NEWS FOR SELECTED TICKER
class NewsUpdater:
    def __init__(self, _ticker):
        self._ticker = _ticker
        self.ticker = self.check_ticker()
        self.ticker_news_api = f'http://next.sigmastock.net/Symbol/GetCompanyNews?sym={self.ticker}&last='
        self.all_news_api = 'http://next.sigmastock.net/Newspaper/GetNewspaper?type=1,2,3,5&last='
        self.news_by_id_api = 'http://next.sigmastock.net/Newspaper/GetNewspaperDetails?id='

    def check_ticker(self):
        try:
            _result = self._ticker.upper()
        except AttributeError:
            return None
        return _result


    def crawl(self,_target):
        _result = rq.get(_target + str(0)).json()
        _result = pd.json_normalize(_result)
        for i in range(6):
            _url = _target + str(_result.iloc[-1,0])
            _df = rq.get(_url).json()
            _df = pd.json_normalize(_df)
            _result = pd.concat([_result,_df])
        _result['upTime'] = _result['upTime'].str.replace(r'T.*','',regex=True)
        _result = _result.set_index('id')
        return _result

    def get_sub_link(self, _title):
        return list(search(_title,num_results=1))[0]

    def run(self):
        if self.ticker == "ALL":
            _df = self.crawl(self.all_news_api)
        else:
            _df = self.crawl(self.ticker_news_api)
        _df['title'] = _df['upTime']+'        '+_df['title']
        _df = _df['title']
        return _df

#print(NewsUpdater('ALL').run().iloc[3])


class EventUpdater:
    def __init__(self):
        self._file_path = f'{main_folder}/temp_/events.csv'
        self.app_ = dict(
            upcoming_event_api='http://sigmastock.net/api/Service/geteventnextweek',
            current_event_api='http://sigmastock.net/api/Service/geteventnow'
        )
        self.api_ =dict(
            headers={
                'authority': 'www.vndirect.com.vn',
                'cache-control': 'max-age=0',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://www.google.com/',
                'accept-language': 'en-US,en;q=0.9',
                'cookie': 'vnds-uuid=2aba2162-6f75-4ebe-8b4f-13d0ae68f520; vnds-uuid-d=1631674721639; _ga=GA1.3.1810566802.1631674723; _gid=GA1.3.1076764156.1633312636; hubspotutk=5b22238e16a541db9597cd374677fd98; __zlcmid=16PkNhLQKilyx6y; _fbp=fb.2.1633578273405.1042301580; PHPSESSID=mstfshvlpvee2ckql9ipvsr0cq; pll_language=vi; _gat_UA-2025955-32=1; __hstc=2186287.5b22238e16a541db9597cd374677fd98.1633403874402.1633578274290.1633654614201.3; __hssrc=1; __hssc=2186287.1.1633654614201',
            },
            url='https://finfo-api.vndirect.com.vn/v4/events?q=locale:VN~effectiveDate:gte:{}~effectiveDate:lte:{}&sort=effectiveDate:asc&size=500'.format(date.today(),date.today() + relativedelta(months=1))
        )

    def is_updated(self):
        try:
            mtime = os.path.getmtime(self._file_path)
        except FileNotFoundError:
            return False
        today = date.today()
        last_modify = date.fromtimestamp(mtime)
        if (last_modify == today) or (today.weekday() in [5, 6]):
            return True
        else:
            return False

    def get_events_by_app(self):
        _df = pd.DataFrame()
        for a in self.app_.keys():
            temp_ = pd.DataFrame()
            _result = rq.get(self.app_[a]).json()
            for r in _result:
                temp_.loc[r['CompanyName'], 'NDKCCDate'] = re.sub("T.*", "", r['NDKCCDate'])
                temp_.loc[r['CompanyName'], 'GDKHQDate'] = re.sub("T.*", "", r['GDKHQDate'])
                temp_.loc[r['CompanyName'], 'Note'] = r['Note']
            _df = pd.concat([_df, temp_], axis=0)
        return _df
    def get_events_by_api(self):
        response = rq.get(self.api_['url'], headers=self.api_['headers']).json()
        data = response[list(response.keys())[0]]
        df = pd.DataFrame.from_dict(data)
        df = df[['code', 'effectiveDate', 'expiredDate', 'note']].set_index('code')
        df.rename(columns={'effectiveDate':'GDKHQDate',
                           'expiredDate':'NDKCCDate',
                           'note':'Note'}, inplace=True)
        return df
    def run(self):
        if self.is_updated():
            print("Daily events data updated")
            _df = pd.read_csv(self._file_path, index_col=0)
        else:
            try:
                _df = self.get_events_by_api()
            except:
                _df = self.get_events_by_app()
            _df.to_csv(self._file_path, encoding='utf-8-sig')
            print(f"Run updater on {date.today()}")
        return _df


# Need to fix parsing data
'''
class OLDEventUpdater:
    def __init__(self):
        self._file_path = f'{main_folder}/temp_/events.csv'
        self.rqUrl = 'https://finance.vietstock.vn/data/eventstypedata'
        self.header = {'Accept': '*/*',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                       'Accept - Encoding': 'gzip, deflate, br',
                       'Accept - Language': 'en - US, en; q = 0.9, vi;q = 0.8, fr - FR;q = 0.7, fr;q = 0.6, tr;q = 0.5',
                       'User-Agent': 'Mozilla/5.0 (Windows  NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
        self.postdata = {'id': 1,
                         'type': 1,
                         'pageSize': 20,
                         'code': '',
                         'catID': -1,
                         'fDate': str((datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')),
                         'tDate': str((datetime.today() + timedelta(days=60)).strftime('%Y-%m-%d')),
                         'page': 1,
                         'orderBy': 'Date1',
                         'orderDir': 'DESC',
                         }

    def is_updated(self):
        try:
            mtime = os.path.getmtime(self._file_path)
        except FileNotFoundError:
            return False
        today = date.today()
        last_modify = date.fromtimestamp(mtime)
        if (last_modify == today) or (today.weekday() in [5, 6]):
            return True
        else:
            return False

    def get_single_event_page(self):
        response = rq.post(self.rqUrl, headers=self.header, data=self.postdata)
        event = response.json()[0]
        _df = pd.DataFrame()
        for e in event:
            _code = e['Code']
            _df.loc[_code, 'CompanyName'] = e['CompanyName']
            _df.loc[_code, 'GDKHQDate'] = e['GDKHQDate']
            _df.loc[_code, 'NDKCCDate'] = e['NDKCCDate']
            _df.loc[_code, 'Note'] = e['Note']
            _df.loc[_code, 'Title'] = e['Title']
        return _df

    def get_event(self):
        _df = pd.DataFrame()
        for self.postdata['eventTypeID'] in [1, 2, 5]:
            self.postdata['page'] = 1
            while True:
                try:
                    part = Sf.parse_time(self.get_single_event_page())
                    _df = pd.concat([_df, part], axis=0)
                    self.postdata['page'] += 1
                except json.decoder.JSONDecodeError:
                    break
        return _df

    def run(self):
        if self.is_updated():
            print("Daily events data updated")
            _df = pd.read_csv(self._file_path, index_col=0)
        else:
            _df = self.get_event()
            _df.to_csv(self._file_path, encoding='utf-8-sig')
            print(f"Run updater on {date.today()}")
        return _df
'''
class AnalysisReportUpdater (NewsUpdater):
    def __init__(self,_ticker):
        self._ticker = _ticker
        self.ticker = self.check_ticker()
        self.analysis_report_api = f"http://next.sigmastock.net/Symbol/GetCompanyNews?sym={self.ticker}&kind=BCPT&last="
        self.analysis_report_all_api = f"http://next.sigmastock.net/Newspaper/GetBCTC?last="
        self.analysis_report_partial_link = "http://next.sigmastock.net/Symbol/GetSymbolContentNews?id="
    def get_sub_link(self, _id):
        _df = rq.get(self.analysis_report_partial_link + str(_id)).json()['content']
        return json.loads(_df)['links'][0]['link']
    def run(self):
        if self.ticker == "ALL":
            _df = self.crawl(self.analysis_report_all_api)
        else:
            try:
                _df = self.crawl(self.analysis_report_api)
            except IndexError:
                return pd.DataFrame()
        for i in _df.index:
            _df.loc[i,"link"] = self.get_sub_link(i)
        return _df


'''
class AnalysisReportUpdater:
    def __init__(self, _ticker):
        self._ticker = _ticker
        self.ticker = self.check_ticker()
        self.analysis_report_api = f"http://next.sigmastock.net/Symbol/GetCompanyNews?sym={self.ticker}&kind=BCPT&last="
        self.analysis_report_all_api = f"http://next.sigmastock.net/Newspaper/GetBCTC?last="
        self.analysis_report_partial_link = "http://next.sigmastock.net/Symbol/GetSymbolContentNews?id="

    def check_ticker(self):
        try:
            _result = self._ticker.upper()
        except AttributeError:
            return None
        return _result

    def get_analysis_table_content(self):
        if self.ticker == "ALL":
            scrape_url = self.analysis_report_all_api
        else:
            scrape_url = self.analysis_report_api

        _result = rq.get(scrape_url).json()
        _df = pd.DataFrame()
        for r in _result:
            try:
                _df.loc[r['Id'], 'Date'] = re.sub("T.*", "", r['CreatedDate'])
                _df.loc[r['Id'], 'Ticker'] = str(r['MCK']).upper()
                _df.loc[r['Id'], 'Title'] = str(r['Title'])
            except TypeError:
                pass
        try:
            return _df.sort_values('Date', ascending=False)
        except KeyError:
            return pd.DataFrame()

    def get_analysis_report_link(self, __id):
        _get_link = rq.get(self.analysis_report_partial_link + str(__id['index'])).json()
        _link = _get_link["LsLink"][0]['Link']
        return _link
'''
# market HNX or VNINDEX
class MarketOverviewData:
    def __init__(self, _market):
        self._market = _market
        self.avgVol20p_api = f"https://mkw-socket.vndirect.com.vn/mkwsocket/marketscatter?index={self._market}"
        self.leader_lage_api = f'https://mkw-socket.vndirect.com.vn/mkwsocket/leaderlarger?index={self._market}'
        self.market_cap_api = f'https://mkw-socket.vndirect.com.vn/mkwsocket/marketcap?index={self._market}'
        self.filter = "HOSE" if self._market == 'VNINDEX' else "HNX"
        self.path_ = f'{main_folder}/temp_/MarketOverviewData.csv'
        # https://mkw-socket.vndirect.com.vn/mkwsocket/foreignmap?index=HOSE giao dich khoi ngoai
        self.market_liquidity_api=f'https://mkw-socket.vndirect.com.vn/mkwsocket/liquidity?index={self._market}'

    def get_data(self):
        # Return the impact of each ticker to the total market, as well as current vol and price
        _leader_large = pd.DataFrame.from_dict(rq.get(self.leader_lage_api).json()['data']).set_index('symbol')
        _market_cap = pd.DataFrame.from_dict(rq.get(self.market_cap_api).json()['data']) \
            .set_index('symbol') \
            .drop(axis=1, columns=['price', 'quantity'])
        _result = pd.concat([_leader_large, _market_cap], axis=1)
        return _result
    def get_current_liquidity(self):
        _market_liquidity = rq.get(self.market_liquidity_api).json()['data'][-1]['value']
        print(rq.get(self.market_liquidity_api).json()['data'][-1])
        return float(_market_liquidity)*1000000000


    def data_cook(self):
        _df = self.get_data()
        _df['vol'] =_df['vol']*10 # cause minimum trading block is 10
        _df['Value'] = _df['price'] * _df['vol']
        total_value = _df['Value'].sum()
        _df['%Value'] = _df['Value'] / total_value
        # Re-calculate percentage of price change:
        _df['percent'] = (_df['price'] - _df['refPrice']) / _df['refPrice']
        _df['MarketEquity'] = _df['price'] * _df['outstandingShares']
        general_info = pd.read_csv(root.loc['General info', 'Path'], index_col=0, usecols=[0, 1, 3])
        _df = pd.concat([_df, general_info], axis=1).dropna(axis=0, how="any", subset=['point'])
        _df = _df[_df['vol'] != 0]
        return _df

    def run(self):
        _df = self.data_cook()
        _df.to_csv(self.path_, encoding="utf-8-sig")
        return _df

class GetMarketOverviewData(MarketOverviewData):
    def __init__(self,market_):
        super().__init__(self)
        self.market= market_
        self.url = f'https://fwtapi1.fialda.com/api/services/app/Market/GetMarketTopSymbols?vnExchange={self.market}&pageSize=10000'
        #foreigner_trading_url=f'https://fwtapi2.fialda.com/api/services/app/Market/GetStatisticalData_Today?exchange={self.market}&sortColumn=Symbol&pageSize=2000'
        self.headers = {
            'authority': 'fwt.fialda.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://fialda.com/',
            'accept-language': 'en-US,en;q=0.9',
        }

    def crawl(self):
        js = rq.get(self.url,headers=self.headers).json()['result']['items']
        df_ = pd.DataFrame.from_dict(js).set_index('symbol')
        return df_

    def data_cook(self):
        status = {
            'Up':'up',
            'Down':'down',
            'Ref':'unchange',
            'Ceil':'ceil',
            'Flr':'floor',
        }
        df_ = self.crawl()
        desire_columns = ['pricePercentChange_52W','capitalization','currentPrice','totalValue','pricePercentChange','status']
        df_ = df_[desire_columns]
        df_['status'].replace(status,inplace=True)
        market_trading_value = df_['totalValue'].sum()
        df_['%Value'] = df_['totalValue']/market_trading_value
        general_info = pd.read_csv(root.loc['General info', 'Path'], index_col=0, usecols=[0, 5, 7])
        df_ = pd.concat([df_, general_info], axis=1).dropna(axis=0, how="any", subset=['capitalization'])
        return df_

class FinancialCrawler:
    '''
    CRAWL THE ENTIRE FINACIAL DATA OF SINGLE STOCK TICKER
    INPUT: STOCK TICKER
    OUTPUT: DATAFRAME AND CSV FILE
    EXTRA:
    - CHECK THE EXISTENCE OF DATA FILE;
    - CHECK IF LAST DATA IS PREVIOUS QUARTER/ YEAR
    '''
    def __init__(self,ticker_):
        self.ticker = str(ticker_).upper()
        self.folder_path = 'D:/Barn/Financial data/vietstock/'
        self.target = dict(
            UrlGetListID={
                'url': 'https://finance.vietstock.vn/data/BCTT_GetListReportData',
                'payload': {
                    'StockCode': self.ticker,
                    'UnitedId': '-1',
                    'AuditedStatusId': '-1',
                    'Unit': '1000000000',
                    'IsNamDuongLich': 'false',
                    'SortTimeType: ': 'Time_ASC',
                    '__RequestVerificationToken': RequestVerificationToken
                }
            },
            UrlGetReportHeaders={
                'url': 'https://finance.vietstock.vn/data/GetListReportNorm_BCTT_ByStockCode',
                'payload': {
                    'StockCode': self.ticker,
                    '__RequestVerificationToken': RequestVerificationToken
                }
            },
            UrlGetReportByID={
                'url': 'https://finance.vietstock.vn/data/GetReportDataDetailValue_BCTT_ByReportDataIds',
            }
        )

    def postingCrawlToDf(self, url_, data_):
        result_ = rq.post(url_, data=data_, headers=headers, cookies=cookies).json()
        result_ = pd.json_normalize(result_['data'])
        return result_

    def termly_crawl (self):
        ListID = self.postingCrawlToDf(self.target['UrlGetListID']['url'], self.target['UrlGetListID']['payload'])
        ReportHeaders = self.postingCrawlToDf(self.target['UrlGetReportHeaders']['url'], self.target['UrlGetReportHeaders']['payload'])
        result_ =pd.DataFrame()
        totalRow = len(ListID.index)

        for i in range(0,totalRow,9):
            reportIDHeader = []
            payload_ = {
                'StockCode': self.ticker,
                'Unit': '1000000000',
                '__RequestVerificationToken': RequestVerificationToken
            }
            for j in range(9):
                if j+i < totalRow:
                    payload_['listReportDataIds[{}][Index]'.format(j)] = j+i
                    payload_['listReportDataIds[{}][ReportDataId]'.format(j)] = ListID.loc[j+i,'ReportDataID']
                    payload_['listReportDataIds[{}][RowNumber]'.format(j)] = ListID.loc[j+i,'RowNumber']
                    payload_['listReportDataIds[{}][YearPeriod]'.format(j)] = ListID.loc[j+i,'YearPeriod']
                    payload_['listReportDataIds[{}][TotalCount]'.format(j)] = totalRow
                    payload_['listReportDataIds[{}][SortTimeType]'.format(j)] = 'Time_ASC'
                    reportIDHeader.append(ListID.loc[j+i,'ReportDataID'])
                    '''if self.target['UrlGetListID']['payload']['PeriodType'] == "QUY":
                        ColHeader.append('Q{}{}'.format(str(ListID.loc[j+i,'ReportTermID']-1),ListID.loc[j+i,'YearPeriod']))
                    else:
                        ColHeader.append('N{}'.format(ListID.loc[j+i, 'YearPeriod']))'''
            separated_df = self.postingCrawlToDf(self.target['UrlGetReportByID']['url'], payload_)
            separated_df = separated_df.set_index('ReportNormId')
            separated_df.drop('ReportTypeCode', inplace=True, axis=1)
            separated_df.dropna(how='all', axis=1, inplace=True)
            separated_df.columns = reportIDHeader
            result_=pd.concat([result_,separated_df],axis=1)

        #RENAME COLUMN HEADER FROM REPORT ID TO PERIOD
        old_header = result_.columns
        new_header = []
        quarter_parse={
            '01':'1',
            '02':'1',
            '03':'1',
            '04':'2',
            '05':'2',
            '06':'2',
            '07':'3',
            '08':'3',
            '09':'3',
            '10':'4',
            '11':'4',
            '12':'4'
        }

        for c in result_.columns:
            try:
                if self.target['UrlGetListID']['payload']['PeriodType'] == "QUY":

                    add_string = 'Q{}{}'.format(
                        quarter_parse[str(ListID.loc[ListID['ReportDataID']==c,'BasePeriodBegin'].iloc[0])[-2:]],
                        str(ListID.loc[ListID['ReportDataID']==c,'BasePeriodBegin'].iloc[0])[:4])
                else:
                    add_string = 'N{}'.format(ListID.loc[ListID['ReportDataID']==c,'YearPeriod'].iloc[0])
                new_header.append(add_string)
            except KeyError:
                result_ = result_.drop(c,axis=1)
        result_.columns = new_header

        #RENAME INDEX FROM REPORT ITEM ID TO ACTUAL NAME

        new_index = []
        for i in result_.index:
            new_index.append(ReportHeaders.loc[ReportHeaders['ReportNormId']==i,'ReportNormName'].iloc[0])
        result_.index=new_index

        #ADD PERIOD ROW TO DIFFERENTIATE FISCAL PERIOD TO CALENDAR PARIOD
        period_ = []
        '''for c in old_header:
            period_.append('{}-{}'.format(ListID.loc[ListID['ReportDataID']==c,'PeriodBegin'].iloc[0]),ListID.loc[ListID['ReportDataID']==c,'PeriodEnd'].iloc[0]))'''
        return result_

    def isUpdated(self):
        try:
            old_ = pd.read_csv(self.folder_path+ self.ticker + ".csv", index_col=0).columns
            current_quarter = (datetime.now().month-1)//3+1
            current_year  =datetime.now().year
            if (current_quarter == 1 and not 'Q{}{}'.format(str(4),str(current_year-1)) in old_)\
                    or not 'Q{}{}'.format(str(current_quarter-1),str(current_year)) in old_\
                    or not 'N{}'.format(str(current_year)) in old_:
                return False
        except FileNotFoundError:
            return False
        print (f'Data of {self.ticker} was updated')
        return True

    def run(self):
        if not self.isUpdated():
            self.target['UrlGetListID']['payload']['PeriodType'] = "NAM"
            result_ = self.termly_crawl()

            time.sleep(random.randint(0, 2))
            self.target['UrlGetListID']['payload']['PeriodType'] = "QUY"
            result_ = pd.concat([result_, self.termly_crawl()], axis=1)
            result_.to_csv(self.folder_path + self.ticker + ".csv", encoding="utf-8-sig")
            time.sleep(random.randint(0, 3))
            print(f'Compete updating for {self.ticker}')
            return result_

class UpdateDatabase:
    '''
    RENEW TICKER LIST, ADD NEW TICKER (IF ANY)
    UPDATE SEPARATED FINANCIAL DATABASE FOR ENTIRE MARKET OR FROM SPECIFIC STICKER
    INPUT:
    -OPTIONAL: DEFAULT BLANK, START TICKER
    -OUTPUT: SEPARATED DATA FILE
    '''
    def __init__(self, _start_at=''):
        self._start_at = _start_at
        self.tickerList = self.get_desired_ticker_list()
        self.general_info_path = root.loc['General info', 'Path']
        self.target= dict(
            generalinfo = {
                'url' : 'https://finance.vietstock.vn/data/corporateaz',
                'payload' : {
                    'catID': 0,
                    'industryID': 0,
                    'page': 1,
                    'pageSize': 50,
                    'type': 1,
                    'code': '',
                    'businessTypeID': 0,
                    'orderBy': 'Code',
                    'orderDir': 'ASC',
                    '__RequestVerificationToken': RequestVerificationToken
                }
            }
        )
        # For next run, add get_general_info in this param:
        '''self.TickerListToUpdate = self.GetTickerListToUpdate()
        self.exist_datafile = self.get_exist_datafile_names()
        self.new_ticker = self.get_new_ticker()'''

    def update_general_info(self):
        def parse_time(string):
            try:
                time_stamp = int(re.findall(r'\d+', string)[0]) / 1000
                date = datetime.fromtimestamp(time_stamp).strftime('%d/%m/%Y')
                return date
            except TypeError:
                return ''
        mtime = os.path.getmtime(self.general_info_path)
        if timedelta.total_seconds(datetime.now()-datetime.fromtimestamp(mtime))/86400 < 7:
            print ("General info updated recently")
            return
        Sf.backup(self.general_info_path)
        df = pd.DataFrame()
        total_pages = 1
        payload_ = self.target['generalinfo']['payload']
        while payload_['page'] <= total_pages:
            result = rq.post(self.target['generalinfo']['url'], data=payload_, headers=headers, cookies=cookies).json()
            result = pd.json_normalize(result)
            total_pages = math.ceil(int(result.loc[0, 'TotalRecord']) / int(payload_['pageSize']))
            payload_['page'] += 1
            df = pd.concat([df, result])
        df.rename(columns={'Code': "Ticker"}, inplace=True)
        df['FirstTradeDate'] = df['FirstTradeDate'].apply(parse_time)
        df.set_index('Ticker', inplace=True, drop=True)
        df.to_csv(self.general_info_path, encoding="utf-8-sig")
        print('Done crawling General info')
        return df

    def get_desired_ticker_list(self):
        _full_tickers = pd.read_csv(root.loc['General info', 'Path'], usecols=[0])['Code'].values.tolist()
        if self._start_at =='':
            return _full_tickers
        else:
            return _full_tickers[_full_tickers.index(self._start_at):]

    def run(self):
        for ticker_ in self.tickerList:
            FinancialCrawler(ticker_).run()

#UpdateDatabase(_start_at='TOT').run()





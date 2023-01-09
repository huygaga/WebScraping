from BarnStructure import root, main_folder, Database, DerivationDatabase
import Support_function as Sf
from DataFetcher import AmibrokerFetch, Dividend, DataUpdater, NewsUpdater, EventUpdater, AnalysisReportUpdater,GetMarketOverviewData,headers
from ChartConfig import combo_chart_layout, pie_chart_layout
import dash
import pandas as pd
import time
import numpy as np

from dash import dash_table
from plotly.subplots import make_subplots
from dash import dcc
from dash import html, ctx
from dash.dependencies import Input, Output, State, MATCH
from dash.dash_table.Format import Format, Group, Scheme
import dash.dash_table.FormatTemplate as FormatTemplate
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import requests as rq
import re
import base64
import datetime
import io

sorted_by = 'Total assets'
compare_unit = 20

temp_path = root.loc['temp_', 'Path']

general_info = pd.read_csv(root.loc['General info', 'Path'], index_col=0)
derivation_database = pd.read_csv(root.loc['vietstock_derivation', 'Path'], index_col=[0, 1])
quarter = derivation_database.filter(regex='^Q').dropna(how='all', axis=0).dropna(how='all', axis=1)
annual = derivation_database.filter(regex='^Y').dropna(how='all', axis=0).dropna(how='all', axis=1)
layout = pd.read_excel(root.loc['Layout', 'Path']).set_index('name')
#layout = pd.read_excel(root.loc['Layout', 'Path'], encoding='utf-8-sig').set_index('name')'
dividend_path = f'{main_folder}/temp_/dividend.csv'
dividend_header = pd.read_csv(dividend_path).columns
dividend = pd.read_csv(dividend_path, usecols=dividend_header[1:-1])

market_overview_data_path = f'{main_folder}/temp_/MarketOverviewData.csv'
color_path = f'{main_folder}/temp_/ColorByMajorIndustry.csv'
color = pd.read_csv(color_path, index_col='IndustryName1')

# For tab3
info = general_info.reset_index()[['Ticker', 'Exchange', 'Name', 'IndustryName1', 'IndustryName2', 'IndustryName3']]

industry_1 = info['IndustryName1'].drop_duplicates()
industry_2 = info['IndustryName2'].drop_duplicates()
industry_3 = info['IndustryName3'].drop_duplicates()

'''Get live update of open price and average trading value'''
price_vol = AmibrokerFetch().run()
'''Get relate event'''
event = EventUpdater().run()[['GDKHQDate', 'NDKCCDate', 'Note']]



def parse_upload_data(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if any(_type in filename for _type in ['csv','txt']):
            # Assume that the user uploaded a CSV file
            _df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')),header=None)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            _df = pd.read_excel(io.BytesIO(decoded),header=None)
    except Exception as e:
        print(e)
        return []
    # To remove header of column
    _result = list(_df.iloc[:,0])
    if len(_result[0])>3:
        _result.pop(0)
    return _result

def get_statistic_table(period):
    deri = derivation_database[period]
    deri = deri.unstack(level=1)
    deri['Ref_price'] = price_vol[price_vol.index.isin(deri.index)]['Close Price'] * 1000
    deri['Trading value (mil)'] = price_vol[price_vol.index.isin(deri.index)]['Value']
    deri['RT P/B'] = deri['Ref_price'] / deri['Book value']
    deri['RT P/E'] = deri['Ref_price'] / deri['EPS']
    deri['ROC P/E'] = (deri['RT P/E'] - deri['P/E']) / deri['P/E']
    deri = deri.round(2).reset_index()
    _market = general_info.reset_index()
    _market.rename(columns={'Code': 'Ticker'}, inplace=True)
    deri = deri.merge(_market[['Ticker', 'Exchange']], how='left', on='Ticker')
    deri.rename(columns={'Exchange': 'Market'}, inplace=True)
    return deri

def get_info_tooltip(df_):
    temp2 = pd.DataFrame()
    temp_ = info[info['Ticker'].isin(list(df_['Ticker']))]
    temp2['Ticker'] = temp_['Ticker'] + ' - ' + temp_['Name']
    return [
        {
            k:
                {'type': 'text', 'value': str(v)} for k, v in row.items()
        } for row in temp2[['Ticker']].to_dict('records')
    ]


def get_template_subplots():
    return make_subplots(rows=3, cols=1,
                         vertical_spacing=0.01,
                         row_heights=[0.4, 0.4, 0.2],
                         shared_xaxes=True,
                         specs=[[{'secondary_y': True}], [{'secondary_y': True}], [{'secondary_y': True}]],
                         subplot_titles=(" ", " "))


def update_layout(fig):
    zeroline_color = 'rgb( 95, 77, 76 )'
    return fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(
            family='Times New Roman',
            color='#7f7f7f',
        ),
        xaxis=dict(
            showgrid=True,
        ),
        xaxis2=dict(
            showgrid=True,
        ),
        xaxis3=dict(
            tickangle=0,
        ),
        yaxis2=dict(
            showgrid=False,
            tickformat=".0%",
            zeroline=True,
            zerolinecolor=zeroline_color,
            zerolinewidth=0.5
        ),
        yaxis4=dict(
            showgrid=False,
            tickformat=".0%",
            side='right',
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            # x=1
        ),
        height=700
    )


def update_layout_tab4(_fig):
    chart_type = _fig['data'][0]['type']
    if chart_type == 'pie':
        return \
            _fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                autosize=False,
                height=350,
            )
    else:
        # bar chart
        return \
            _fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                autosize=False,
                width=1250,
                height=350,
                xaxis_title='',
                yaxis=dict(tickformat=".0%"),
            )


def get_sub_plot_layout(ticker):
    industry2 = general_info.loc[ticker, 'IndustryName2']
    if industry2 == 'Trung gian tín dụng và các hoạt động liên quan':
        s_layout = layout[layout['industry'].isin(['Trung gian tín dụng và các hoạt động liên quan', 'Toàn bộ'])]
    else:
        s_layout = layout[layout['industry'].isin(['Khác', 'Toàn bộ'])]
    return s_layout


def get_similar_company(ticker):
    _info = general_info.loc[ticker , :]
    df = general_info[(general_info['IndustryName2'] == _info['IndustryName2']) & (general_info['IndustryName3'] == _info['IndustryName3'])]
    return df


def get_similar_company_data(temporal_database, ticker):
    similar_tickers = get_similar_company(ticker)
    similar_data = temporal_database[temporal_database.index.get_level_values(0).isin(similar_tickers.index)].dropna(
        how='all', axis=1)
    most_recent = similar_data.columns[1]
    temp = similar_data[similar_data.index.get_level_values(1) == sorted_by].sort_values(most_recent, ascending=False)
    try:
        sorted_index = Sf.shift_to_top(list(temp.index.get_level_values(0)), ticker)
        similar_data = similar_data.reindex(sorted_index, level=0)
        return similar_data
    except ValueError:
        print(f'Data for {ticker} has NOT been updated')
        return None


def shrink_dataframe(_similardata, _size):
    shrinked = _similardata.loc[_similardata.index.get_level_values(0).unique()[:_size].tolist()] \
        .dropna(how='all', axis=1)
    return shrinked



def data_format_by_columns(list__):
    columns = [{"name": i,
                "id": i,
                "selectable": True,
                'type': 'numeric',
                } for i in list__]
    format_template = dict(
        integer=dict(
            name=layout[layout["data_format"] == "Integer"].index,
            format=Format(
                scheme=Scheme.fixed,
                precision=0,
                group=Group.yes,
                groups=3,
                group_delimiter=',',
                decimal_delimiter='.')
        ),
        float=dict(
            name=layout[layout["data_format"] == "Float"].index,
            format=Format(
                scheme=Scheme.fixed,
                precision=2,
                group=Group.yes,
                groups=3,
                group_delimiter=',',
                decimal_delimiter='.')
        ),
        percentage=dict(
            name=layout[layout["data_format"] == "Percentage"].index,
            format=FormatTemplate.percentage(1)
        )
    )
    for col in columns:
        for key in format_template.keys():
            if col['name'] in format_template[key]['name']:
                col['format'] = format_template[key]['format']
            else:
                pass
    return columns


def expand(__str):
    return f"{__str} expand"


def collapse(__str):
    return str(__str).replace(" expand", "")


def get_data_by_industry(_df, inds):
    _df2 = _df.groupby(inds).sum()
    if len(_df2.index) >= 10:
        # Get top of industry
        _df3 = _df2.sort_values('%Value', ascending=False)[:9]
        # Sum the rest
        _temp = _df2.sort_values('%Value', ascending=False)[9:]
        _temp2 = _temp['%Value'].sum()
        _df3.loc['Others', '%Value'] = _temp2
    else:
        _df3 = _df2.sort_values('%Value', ascending=False)
    return _df3.reset_index()


def candle_type(row):
    if row['pricePercentChange']>0:
        type_='up'
    elif row['pricePercentChange']<0:
        type_='down'
    else:
        type_='unchange'
    return type_


def get_color_discrete_map(df_,return_type='dict'):
    color_ = {
        'up': '#0CE84A',
        'down': '#E84427',
        'unchange': '#E8DD0C',
        'ceil': '#E81780',
        'floor': '#1DDBDB',
    }
    if return_type=='dict':
        color_dict = {i: color_[i] for i in list(df_['status'].drop_duplicates())}
        color_dict['(?)'] = '#ffffff'
        return color_dict
    elif return_type=='df':
        temp_ = df_['status']
        temp_.replace(color_,inplace=True)
        return temp_
    else:
        df_['color'] = df_.apply(candle_type, axis=1)
        return [color_[i] for i in df_['color']]

def getGeneralCompanyLiveParams(ticker):
    url = 'https://finance.vietstock.vn/company/tradinginfo'
    cookies_ = {
        'ASP.NET_SessionId': '0dousw3w0wl2hxtqgktm1ov1',
        '__RequestVerificationToken': 'QXokBWQjpNNzoQ9LVDhiG9h2gRjgpO-6XnNMKxZVs4fWMXH2ZsQMhBJRvRaXGqFYGDWQw2LPTPU_Uk_d_4sPqzalbvIMY9KFkTNtRBcclRA1',
    }
    payload = {
        'code': ticker,
        's': '1',
        '__RequestVerificationToken': 'KxX69vEChRckjVuvrk8eVRKYtaH1XYoYoExEmNPzWoX1iYI6-xHYnO45LVgeYM9sw5xksROhpiRsf-N_1JVAA1bWOzjE-hffnnRW0vUnVQA1'
    }
    response=rq.post(url,headers=headers,data=payload,cookies=cookies_).json()
    result = pd.DataFrame.from_dict(response,orient="index")
    result = result[result.index.isin(['KLCPLH','KLCPNY','MarketCapital','Beta','EPS','PE','PB','RemainRoom'])]
    result = result.transpose()
    for c in result.columns:
        if layout.loc[c,"data_format"] == 'Float':
            result[c] = result[c].apply(lambda x:"{:.2f}".format(x))
        elif layout.loc[c,"data_format"] == 'Integer':
            result[c] = result[c].apply(lambda x: "{:,}".format(x))
        elif layout.loc[c,"data_format"] == 'Percentage':
            result[c] = result[c].apply(lambda x: "{:.2%}".format(x/100))
        else:
            continue
    result = result.transpose().reset_index()
    result.columns=['index',"value"]
    return result

empty_start_table = pd.DataFrame(columns=['Choose desired industry then press GO'])
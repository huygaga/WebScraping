'''
TEST SHARE HOLDERS PIE CHART
'''

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
import plotly.express as px
from Controller import *

# VIETSTOCK PARAMS:
separated_datafiles_container = f'{main_folder}/Financial data/vietstock'

#Below RequestVerificationToken is for payload, different from one for cookies
RequestVerificationToken = 'eR1ewuUbhLPC9Ntoh656a7GiSGUKlD3CQH77-kjmDmklRl65tQ9KU9FTvwuuhjmD6KdQFeym40fTOZLrh9wV1Pn8eG2abp-6pnw_3v7OG42Pfb3LTeqgIDeubUYzYU5l0'
cookies = {
    '_ga': 'GA1.2.964262963.1626950717',
    '__gpi': '00000000-0000-0000-0000-000000000000',
    'dable_uid': '16539417.1635908622258',
    'language': 'vi-VN',
    'Theme': 'Light',
    'AnonymousNotification': '',
    '_gid': 'GA1.2.1368452260.1644898505',
    'ASP.NET_SessionId': 'yh4zfjbvjkc0red5nraizrw1',
    '__RequestVerificationToken': 'Is121mDbIZzMPohHDVPlOH0RXqA4ij-S5P5JHuZLR9p0jgDH3Zz-arLhOnM4Xh9RKYzwYJWh1GUWBZBS3s6WYyPTWDCvSGFZGZrL2bMd08M1',
    'finance_viewedstock': 'MPC,CMX,DAH,SMC,',
    'vts_usr_lg': 'D304F05C4099047FF246BFC0AD55C9D4FBDE8ADDE0A115E55C14F23754C8A933105EBA4BED80D0BD46ADF001D22827152715C0842A93186917645C3AE356360086041A4953AD446929EE2404485A29CB3FF846FB93EE1685849A1D0D80F0B1DD936B68976D3D8F6B8FA87D0B7CDD52E4B44C5993B7B0286662D97460CFECD7AC',
    'vst_usr_lg_token': 'y9PXsItJI0SB++zJiB6FkQ==',
    '__gads': 'ID=49d83561c7781495-220c64e2a5d0005a:T=1636094718:RT=1645157219:S=ALNI_MY3kM2tr79pHNMD3qvAAVa0xfRLUQ',
}
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
}

def getGeneralCompanyInfo(ticker):
    url = f'https://svr2.fireant.vn/api/Data/Companies/MajorHolders?symbol={ticker}'
    response=rq.get(url).json()
    response = pd.DataFrame.from_dict(response)[['Name','Position',"Ownership","IsOrganization",'IsForeigner','IsFounder']]
    response.loc[len(response.index),["Name",'Ownership']]=["Other",1-(response['Ownership'].sum())]
    return response
df= getGeneralCompanyInfo("VNM")

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(
        id="pie-chart",
        figure=go.Figure(
            data=go.Pie(
                labels=df['Name'],
                values=df['Ownership'],
                hoverinfo="label+percent",
                textinfo='label',
                insidetextorientation='radial',
                showlegend=False,
                textposition='inside'
            )
        )
    ),
])


if __name__ == '__main__':
    app.run_server(port=8051,debug=True)  # debug=True

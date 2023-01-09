from Controller import *
from googlesearch import search

app = dash.Dash(__name__)
app.layout = \
    html.Div(
        className='twelve columns',
        children=[
            # HEADER
            html.Div([
                # TAB1/ TAB2
                html.Div(
                    id='info_header',
                    children=[
                        html.Div(
                            className='text two columns',
                            children=[
                                html.Form(
                                    style={'height': '45%'},
                                    children=[
                                        html.Label("Ticker"),
                                        dcc.Input(id="input_ticker", placeholder="Ticker", style={'width': '100%'}),
                                    ]
                                ),
                                html.Form(
                                    style={'height': '45%'},
                                    children=[
                                        html.Label("Period"),
                                        dcc.Dropdown(
                                            id='period_dropdown', style={'width': '100%'},
                                            options=[
                                                {'label': 'Quarterly', 'value': 'Quarterly'},
                                                {'label': 'Annual', 'value': 'Annual'}],
                                            value='Quarterly',
                                        ),
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            id='ticker_properties',
                            className='text ten columns'
                        )
                    ]),
                # TAB3
                html.Div(
                    id='graph_header',
                ),
            ]),
            # BODY: GRAPHING & TABULATION
            html.Div(
                style={'display': 'block'},
                className='twelve columns',
                children=[
                    dcc.Tabs(
                        id='tabs',
                        value='tab1',
                        children=[
                            dcc.Tab(
                                id='tab1',
                                value='tab1',
                                label='Financial Report',
                            ),
                            dcc.Tab(
                                id='tab2',
                                value='tab2',
                                label='Comparison',
                                children=[
                                    html.Div([
                                        html.Label("Time Period"),
                                        dcc.Slider(id="time_slider", value=1, included=False),
                                    ]),
                                    dcc.Graph(
                                        id='graph2',
                                    ),
                                    html.Div(id='intermediate-value', style={'display': 'none'})
                                ],
                            ),
                            dcc.Tab(
                                id='tab3',
                                value='tab3',
                                label='Statistic',
                                children=[
                                    html.Div(children=[
                                        html.Div(
                                            className="twelve columns",
                                            id='control panel tab3',
                                            children=[
                                                html.Div(
                                                    className='eight columns',
                                                    children=[
                                                        # market market_list
                                                        dcc.Dropdown(
                                                            id='market_list',
                                                            options=[
                                                                {'label': 'HOSE', 'value': 'HOSE'},
                                                                {'label': 'HNX', 'value': 'HNX'},
                                                                {'label': 'UPCoM', 'value': 'UPCoM'},
                                                            ],
                                                            value=['HOSE', 'HNX', 'UPCoM'],
                                                            multi=True,
                                                            className="four columns"
                                                        ),
                                                        # html.Label('Industry 1'),
                                                        dcc.Dropdown(
                                                            placeholder='Ngành cấp 1',
                                                            options=[{'label': i, 'value': i} for i in industry_1],
                                                            id='industry_1',
                                                            optionHeight=60,
                                                            className="two columns",
                                                        ),
                                                        dcc.Dropdown(
                                                            placeholder='IndustryName2',
                                                            # options=[{'label': i, 'value': i} for i in industry_2],
                                                            id='industry_2',
                                                            optionHeight=60,
                                                            className="two columns",
                                                        ),
                                                        dcc.Dropdown(
                                                            placeholder='IndustryName3',
                                                            # options=[{'label': i, 'value': i} for i in industry_3],
                                                            id='industry_3',
                                                            optionHeight=60,
                                                            className="two columns",
                                                        ),
                                                        dcc.Dropdown(
                                                            className="two columns",
                                                            options=[{'label': i, 'value': i} for i in
                                                                     derivation_database.columns],
                                                            value='Q3 2022',
                                                            id='period',
                                                            optionHeight=60,
                                                        )
                                                    ]),
                                                html.Div(
                                                    className='four columns tight right',
                                                    children=[
                                                        html.Button(
                                                            children=[
                                                                dcc.ConfirmDialogProvider(
                                                                    id='confirm box',
                                                                    children=[
                                                                        html.Img(
                                                                            title="Copy to clipbboard",
                                                                            src=app.get_asset_url(
                                                                                "copy_to_clipboard.png"),
                                                                            className="button_image",
                                                                        )
                                                                    ],
                                                                )],
                                                            className='two columns right tight btn btn-outline-success'),
                                                        html.Button(
                                                            children=[
                                                                dcc.Upload(
                                                                    id='upload_data',
                                                                    children=[
                                                                        html.Img(
                                                                            title='Upload',
                                                                            id='upload_button',
                                                                            className='button_image',
                                                                            src=app.get_asset_url('upload.png')
                                                                        )],
                                                                )],
                                                            className='two columns right tight btn btn-outline-success'
                                                        ),
                                                        html.Button('Current Industry', id='current_industry',
                                                                    className='four columns right btn btn-outline-success'),
                                                        html.Button('GO', id='go_button',
                                                                    className='four columns right btn btn-outline-success'),
                                                    ]),
                                            ]),
                                        html.Div(
                                            className='twelve columns',
                                            id='table-container',
                                            children=[
                                                html.Div(
                                                    style={'padding-left': 30},
                                                    children=[
                                                        dash_table.DataTable(
                                                            id='total_row',
                                                            data=empty_start_table.to_dict('records'),
                                                            columns=[{'id': c, 'name': c} for c in
                                                                     empty_start_table.columns],
                                                            css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                                                            style_header={'display': 'none'},
                                                            style_cell={'font-family': 'Times New Roman',
                                                                        'color': 'white',
                                                                        'backgroundColor': '#5399C7',
                                                                        'border': '1px solid white',
                                                                        'vertical-align': 'middle',
                                                                        'text-align': 'center',
                                                                        },
                                                        ),
                                                    ]
                                                ),
                                                dash_table.DataTable(
                                                    id='data_table',
                                                    data=empty_start_table.to_dict('records'),
                                                    columns=[{'id': c, 'name': c} for c in empty_start_table.columns],
                                                    # editable=True,
                                                    filter_action="native",
                                                    sort_action="native",
                                                    sort_mode="multi",
                                                    # column_selectable="single",
                                                    row_selectable="multi",
                                                    # row_deletable=True,
                                                    selected_columns=[],
                                                    selected_rows=[],
                                                    page_action="native",
                                                    page_current=0,
                                                    page_size=20,
                                                    style_header={'whiteSpace': 'normal',
                                                                  'vertical-align': 'middle',
                                                                  'text-align': 'center',
                                                                  'color': 'white',
                                                                  'backgroundColor': '#5399C7',
                                                                  'border': '1px solid white'
                                                                  },
                                                    css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                                                    style_cell={'font-family': 'Times New Roman'},
                                                    style_data_conditional=[
                                                                               {
                                                                                   'if': {'row_index': 'odd'},
                                                                                   'backgroundColor': '#E9F2F8'
                                                                               }
                                                                           ] + [
                                                                               {
                                                                                   'if': {
                                                                                       'filter_query': '{ROC P/E} < 0',
                                                                                       'column_id': 'ROC P/E'
                                                                                   },
                                                                                   'color': 'tomato',
                                                                               }
                                                                           ] + [
                                                                               {
                                                                                   'if': {
                                                                                       'filter_query': '{ROC P/E} >= 0',
                                                                                       'column_id': 'ROC P/E'
                                                                                   },
                                                                                   'color': '#00b261',
                                                                               }
                                                                           ],
                                                    style_cell_conditional=
                                                    [
                                                        {'if': {'column_id': c}, 'border-left': '1.5px solid #5399C7'}
                                                        for c in
                                                        ['Net profit', 'AGR Net Interest', 'AGR Net Profit', 'Equity',
                                                         'ROA', 'P/E',
                                                         'P/B', 'Trading value (mil)']
                                                    ]
                                                )
                                            ]),
                                    ])
                                ]),
                            dcc.Tab(
                                id='tab4',
                                value='tab4',
                                label='Market Trading Overview',
                                children=[
                                    html.Div([
                                        html.Div([
                                            html.Button('Refresh', id='refresh_button',
                                                        className='nine columns left btn-outline-success'),
                                            html.Form(
                                                [dcc.Dropdown(id='market', style={'height': '100%', 'width': '100%'},
                                                              options=[
                                                                  {'label': 'VNINDEX', 'value': 'HSX'},
                                                                  {'label': 'HNXINDEX', 'value': 'HNX'},
                                                                  {'label': 'UPCOM', 'value': 'UPCOM'}],
                                                              value='HSX')],
                                                className='three columns'),
                                        ], style={'height': '40px'}),
                                        html.Div(id='statistic_container', style={'display': 'none'})
                                    ])
                                ],
                            )
                        ])
                ]),
            # ----------------- SIDEBAR ------------------------------------
            html.Div(
                children=[
                    html.Button(
                        id="optionbtn",
                        className="openbtn",
                        children="Option"
                    ),
                    html.Button(
                        id="dividendbtn",
                        className="openbtn",
                        children="Dividend"
                    ),
                    html.Button(
                        id="analysis_report_btn",
                        className="openbtn",
                        children="Analysis Report"
                    ),
                    html.Button(
                        id="news_btn",
                        className="openbtn",
                        children="News"
                    ),
                    html.Div(
                        id="option_sidebar",
                        className="sidebar",
                        children=[
                            html.Ul(
                                children=[
                                    html.Button(
                                        id="get_dividend",
                                        className="button btn-outline-success",
                                        children="Get Market Dividend data"
                                    ),
                                    dbc.Toast(
                                        id="get_dividend_notification",
                                        header="Notification",
                                        is_open=False,
                                        duration=4000,
                                        style={"position": "fixed", "bottom": 66, "left": 10, "width": 350},
                                    ),
                                    html.Button(
                                        id="update_individual_findata",
                                        className="button btn-outline-success",
                                        children="Update Findata for current Ticker"
                                    ),
                                    dbc.Toast(
                                        id="update_individual_findata_notification",
                                        header="Notification",
                                        is_open=False,
                                        duration=4000,
                                        style={"position": "fixed", "bottom": 66, "left": 10, "width": 350},
                                    ),
                                    html.Button(
                                        id="update_market_findata",
                                        className="button btn-outline-success",
                                        children="Update Findata for Entire market \n(Supper slow)"
                                    ),
                                    dbc.Toast(
                                        id="update_market_findata_notification",
                                        header="Notification",
                                        is_open=False,
                                        duration=4000,
                                        style={"position": "fixed", "bottom": 66, "left": 10, "width": 350},
                                    ),
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        id="dividend_sidebar",
                        className="sidebar",
                    ),
                    html.Div(
                        id="analysis_report_sidebar",
                        className="sidebar",
                    ),
                    html.Div(
                        id="news_sidebar",
                        className="sidebar"
                    ),
                    html.Div(
                        id="toggle_switch",
                        style={'display': 'none'},
                        children=[]
                    )
                ],
                id='sidebar'),
        ])

"""--------------       HEADER CALLBACK       --------------------"""


# TO CHANGE HEADER BASE ON SELECTED TAB:
@app.callback(
    [Output(component_id='info_header', component_property='style'),
     Output(component_id='graph_header', component_property='style')],
    [Input(component_id='tabs', component_property='value')])
def change_header_type(tab):
    if tab == 'tab3':
        return {'display': 'none', }, {'display': 'block', 'height': '150px'}
    elif tab == 'tab4':
        return {'display': 'none', }, {'display': 'none', }
    else:
        return {'height': '150px'}, {'display': 'none'}


# UPDATE HEADER OF TAB1/ TAB2: TICKER NAME & PROPERTIES
@app.callback(
    Output(component_id='ticker_properties', component_property='children'),
    Input(component_id='input_ticker', component_property='value'))
def update_properties(input_):
    try:
        if len(input_) == 3:
            input_ = input_.upper()

            ticker_info = general_info.loc[input_, :]

            _event = event[event.index == input_]

            _tooltip_table = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in _event.columns],
                data=_event.to_dict('records'),
            )
            ticker_properties_df = getGeneralCompanyLiveParams(input_)

            _result = [
                html.Div(
                    id='ticker_name',
                    className='text eight columns',
                    children=[
                        html.H1(children=dcc.Link(children=[input_ if len(_event.index) == 0 else input_ + "*"],
                                                  href=f'https://finance.vietstock.vn/{input_}/ho-so-doanh-nghiep.htm',
                                                  target='_blank',
                                                  style={'color': 'rgb(38 114 165)', 'text-decoration': 'none'}),
                                id='ticker_title',
                                ),
                        dbc.Tooltip(
                            children=['' if len(_event.index) == 0 else _tooltip_table],
                            target='ticker_title',
                            placement="right"
                        ),
                        html.H3(children=ticker_info['Name']),
                        html.P(['{} \ {} \ {}'.format(ticker_info['IndustryName1'], ticker_info['IndustryName2'],
                                                      ticker_info['IndustryName3'])],
                               style={'font-size': '2.0rem', 'font-style': 'italic', 'word-wrap': 'break-word'})
                    ]
                ),
                html.Div(
                    className='text four columns',
                    children=
                        dash_table.DataTable(
                            id='ticker_properties_table',
                            data=ticker_properties_df.to_dict('records'),
                            columns=[{"name": i, "id": i} for i in ticker_properties_df.columns],
                            style_header={'display': 'none', 'height': 0},
                            style_cell={'font-family': 'Times New Roman', 'border': 'none'},
                            style_table={'height':'100px'},
                            virtualization=True
                        )

                )
            ]
            return _result
        else:
            return [None]
    except (IndexError, KeyError, TypeError):
        return [None]


# UPDATE HEADER OF TAB 3: GRAPHING
@app.callback(
    Output(component_id='graph_header', component_property='children'),
    [Input(component_id='data_table', component_property='derived_virtual_selected_rows'),
     Input(component_id='period', component_property='value')],
    [State(component_id='data_table', component_property='derived_virtual_data')]
)
def update_graph_header(selected_rows, period, derived_virtual_data):
    color_ = ['rgb(38, 70, 83)', 'rgb(231, 111, 81)', 'rgb(42, 157, 143)', 'rgb(233, 196, 106)', 'rgb(244, 162, 97)']
    plot_indicator = ["EPS", "P/B", "P/E", "ROA", "ROE"]
    df_ = pd.DataFrame(derived_virtual_data)
    if df_.empty or len(selected_rows) == 0:
        return dash.no_update
    else:
        selected_tickers = list(df_.iloc[selected_rows, 0])

        to_show = derivation_database[derivation_database.index.get_level_values(0).isin(selected_tickers)]
        columns = pd.Series(to_show.columns).str.startswith(str(period)[0])
        to_show = to_show[to_show.columns[columns]].dropna(how='all', axis=1)
        to_show = to_show.iloc[:, :(12 if len(to_show.columns) >= 12 else len(to_show.columns))]  # limit period to 12
        fig3 = make_subplots(rows=1, cols=2,
                             horizontal_spacing=0.05,
                             specs=[[{'secondary_y': True}, {'secondary_y': True}]])
        s_layout = get_sub_plot_layout(selected_tickers[0])
        s_layout = s_layout[(s_layout['type'] == 'scatter') & (s_layout.index.isin(plot_indicator))]
        x3 = to_show.columns
        for i in range(len(selected_tickers)):
            for name in s_layout.index:
                try:
                    y3 = to_show.loc[(selected_tickers[i], name), :]
                    fig3.add_trace(go.Scatter(x=x3, y=y3,
                                              mode='lines',
                                              name=f'{(selected_tickers[i])}- {name}',
                                              line=dict(
                                                  color=color_[i],
                                                  width=s_layout.loc[name, 'width'],
                                                  dash=s_layout.loc[name, 'dash'])
                                              ),
                                   secondary_y=s_layout.loc[name, 'secondary_y'],
                                   row=1,
                                   col=int(s_layout.loc[name, 'row']) - 1)  # Tranpose to 1 row, 2 col
                except KeyError:
                    print(name)
                    continue

        fig3.update_layout(
            margin=dict(l=0, r=0, t=0, b=0, pad=0),
            height=140,
            showlegend=False,
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
            yaxis2=dict(
                showgrid=False,
                tickformat=".1%",
            ),
            yaxis4=dict(
                showgrid=False,
                tickformat=".1%",
                side='right',
            ),
            legend=dict(
                yanchor="top",
                y=0.8,
                xanchor="right",
            ),
        )

    return dcc.Graph(figure=fig3)


"""---------------------       TAB1 / TAB2       -----------------------------"""


# GET DATABASE FOR SIMILAR COMPANIES AS WELL AS CURRENT TICKER:
@app.callback(
    Output(component_id='intermediate-value', component_property='children'),
    [Input(component_id='input_ticker', component_property='value'),
     Input(component_id='period_dropdown', component_property='value')]
)
def get_intermediate_database(ticker, period):
    if period == "Annual":
        database = annual
    else:
        database = quarter
    try:
        if len(ticker) == 3:
            ticker = ticker.upper()
            similar_data = get_similar_company_data(database, ticker)
            similar_data = shrink_dataframe(similar_data, compare_unit).dropna(how='all', axis=1)
            similar_data.to_csv(temp_path, encoding="utf-8-sig")
            return ticker
    except (KeyError, TypeError, IndexError):
        return dash.no_update


# TO UPDATE GRAPH AT TAB1
@app.callback(
    [Output(component_id='tab1', component_property='children')],
    [Input(component_id='intermediate-value', component_property='children')]
)
def update_graph(__ticker):
    def get_time_axis_label(l):
        l = [li.replace('Q1 ', 'Q1<br>') for li in l]
        l = [re.sub(r'( \d*)', '', li) for li in l]
        return l

    def get_background_shape_coordinates(xaxis_values):
        x_coordinates = []
        temp_ = [re.search(r'(\d{4})', x).group(1) for x in xaxis_values]
        unique_ = list(dict.fromkeys(temp_))
        for u in unique_:
            for i in range(len(temp_)):
                if temp_[i] == u:
                    count = temp_.count(u)
                    x_coordinates.append([xaxis_values[i], xaxis_values[i + count - 1]])
                    break
        return x_coordinates

    try:
        if len(__ticker) == 3:
            fig1 = get_template_subplots()
            similar_data = pd.read_csv(temp_path, index_col=[0, 1])
            s_layout = get_sub_plot_layout(__ticker)

            # GET PLOT DATA
            to_plot_tab1 = shrink_dataframe(similar_data, 1)
            x1 = to_plot_tab1.columns

            # r1c1_secondary_y_data = pd.Series(dtype='float64')
            for name in s_layout.index:
                if Sf.is_nan(s_layout.loc[name, 'type']):
                    continue
                else:
                    y1 = to_plot_tab1.loc[(__ticker, name), :]
                    fig1.add_trace(Sf.trace_data(s_layout, name, x1, y1),
                                   secondary_y=s_layout.loc[name, 'secondary_y'],
                                   row=int(s_layout.loc[name, 'row']), col=int(s_layout.loc[name, 'col']))
                    if s_layout.loc[name, 'secondary_y'] == True and int(s_layout.loc[name, 'row']) == 1:
                        __temp = pd.Series(y1, dtype='float64')
                        # r1c1_secondary_y_data = r1c1_secondary_y_data.append(y1)
            update_layout(fig1)

            '''area_ = get_background_shape_coordinates(x1)
            for i in range(0,len(area_),2):
                fig1.add_vrect(
                    x0=area_[i][1], x1=area_[i][0],
                    fillcolor="LightSalmon", #opacity=0.5,
                    #layer="above", line_width=0,
                    row='all',col=[1],
                    yref='paper'
                )'''

            # To change x axis label
            x1_tickvals = [i for i in range(len(to_plot_tab1.columns))]
            x1_ticktext = get_time_axis_label(x1)
            fig1.update_layout(
                xaxis3=dict(
                    tickvals=x1_tickvals,
                    ticktext=x1_ticktext
                )
            )

            return [dcc.Graph(figure=fig1, id='graph1')]
        else:
            return dash.no_update
    except (KeyError, TypeError):
        return dash.no_update


# TO UPDATE GRAPH AT TAB2
@app.callback(
    Output(component_id='graph2', component_property='figure'),
    [Input(component_id='intermediate-value', component_property='children'),
     Input(component_id='time_slider', component_property='value')],
    State(component_id='time_slider', component_property="marks")
)
def update_graph(ticker, value, mark):
    try:
        if len(ticker) == 3:
            fig2 = get_template_subplots()
            to_plot_tab2 = pd.read_csv(temp_path, index_col=[0, 1])
            # GET PERIOD FROM SLIDER'S MARKS:
            _period = mark[str(value)]

            shrink_indexes = to_plot_tab2.index.get_level_values(0).drop_duplicates(keep='first')

            s_layout = get_sub_plot_layout(shrink_indexes[0])
            x2 = [i + '<br>' + general_info.loc[i, 'Ticker'] for i in shrink_indexes]
            for name in s_layout.index:
                if Sf.is_nan(s_layout.loc[name, 'type']):
                    continue
                else:
                    y2 = to_plot_tab2[to_plot_tab2.index.get_level_values(1) == name].loc[:, _period]
                    fig2.add_trace(Sf.trace_data(s_layout, name, x2, y2),
                                   secondary_y=s_layout.loc[name, 'secondary_y'],
                                   row=int(s_layout.loc[name, 'row']), col=int(s_layout.loc[name, 'col']))

            update_layout(fig2)
            fig2.update_traces(mode='lines+markers', line=dict(width=1), marker={'size': 3},
                               selector=dict(type='scatter'))
            return fig2
        else:
            return dash.no_update
    except (KeyError, TypeError):
        return dash.no_update


# TO UPDATE SLIDER IN TAB2
@app.callback(
    [Output(component_id='time_slider', component_property="marks"),
     Output(component_id='time_slider', component_property="min"),
     Output(component_id='time_slider', component_property="max"),
     Output(component_id='time_slider', component_property="value"),
     ],
    [Input(component_id='intermediate-value', component_property='children')],
    State(component_id='time_slider', component_property='value')
)
def make_slider_properties(_input, _value):
    _mark_label = pd.read_csv(temp_path, index_col=[0, 1]).columns
    _max = min(20, len(_mark_label))
    _mark = {i: _mark_label[i] for i in range(_max)}
    _min = 0
    return _mark, _min, _max, _value


"""---------------------       TAB3       -----------------------------"""


# UPDATE INDUSTRY 2 BASED ON INDUSTRY 1
@app.callback(
    Output(component_id='industry_2', component_property='options'),
    [Input(component_id='industry_1', component_property='value')])
def update_industry_2_options(value):
    options = info[info['IndustryName1'] == value]['IndustryName2'].drop_duplicates()
    return [{'label': i, 'value': i} for i in options]


# UPDATE INDUSTRY 3 BASED ON INDUSTRY 2
@app.callback(
    Output(component_id='industry_3', component_property='options'),
    [Input(component_id='industry_2', component_property='value')])
def update_industry_3_options(value):
    options = info[info['IndustryName2'] == value]['IndustryName3'].drop_duplicates()
    return [{'label': i, 'value': i} for i in options]


# GET SIMILAR COMPANY TO ASSESSING COMPANY IN TAB1
@app.callback(
    [Output(component_id='industry_1', component_property='value'),
     Output(component_id='industry_2', component_property='value'),
     Output(component_id='industry_3', component_property='value')],
    Input(component_id='current_industry', component_property='n_clicks'),
    State(component_id='input_ticker', component_property='value')
)
def get_current_industry(n_clicks, input_):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            if len(input_) == 3:
                input_ = input_.upper()
                ticker_info = general_info.loc[input_, :]
                return ticker_info['IndustryName1'], ticker_info['IndustryName2'], ticker_info['IndustryName3']
        except (KeyError, TypeError):
            return dash.no_update


# UPDATE DATATABLE AS GO_BUTTON PRESSED OR UPLOAD DATA FILE
@app.callback(
    [Output(component_id='data_table', component_property='columns'),
     Output(component_id='data_table', component_property='data'),
     Output(component_id='data_table', component_property='tooltip_data')],
    [Input(component_id='go_button', component_property='n_clicks'),
     Input(component_id='upload_data', component_property='contents')],
    [State(component_id='industry_1', component_property='value'),
     State(component_id='industry_2', component_property='value'),
     State(component_id='industry_3', component_property='value'),
     State(component_id='period', component_property='value'),
     State(component_id='market_list', component_property='value'),
     State(component_id='upload_data', component_property='filename')
     ]
)
def update_table(n_clicks, upload_content, ind1, ind2, ind3, period, market, upload_filename):
    # Get name of button which be the most recently clicked
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if (n_clicks is None or market == []) and upload_content is None:
        raise PreventUpdate
    else:
        table = get_statistic_table(period)
        if 'upload_data' in changed_id:
            ticker = parse_upload_data(upload_content, upload_filename)
        else:
            if ind1 is None and ind2 is None and ind3 is None:
                ticker = info[info['Exchange'].isin(market)]['Ticker']
            else:
                ticker = info[info['Exchange'].isin(market)
                              & (info['IndustryName1'] == ind1)
                              & (info['IndustryName2'] if ind2 is None else (info['IndustryName2'] == ind2))
                              & (info['IndustryName3'] if ind3 is None else (info['IndustryName3'] == ind3))]['Ticker']

        table = table[table['Ticker'].isin(ticker)].dropna(axis=1, how='all')
        table.dropna(how="any", subset=["EPS"])

        # Re-order table columns:
        # table = table[table['Equity'] > 0]
        columns_template = layout[layout["order_in_statistic_table"] > 0].sort_values(
            by=["order_in_statistic_table"]).drop_duplicates()
        desired_columns = []

        for i in columns_template.index:
            if i in table.columns:
                desired_columns.append(i)
            else:
                continue
        table = table[desired_columns]


        tooltip_data_ = get_info_tooltip(table)

        columns = data_format_by_columns(list(table.columns))
        data = table.to_dict('records')
        return columns, data, tooltip_data_


# GET SUMMARY ROW
@app.callback(
    [Output(component_id='total_row', component_property='columns'),
     Output(component_id='total_row', component_property='data')],
    [Input(component_id='data_table', component_property='derived_virtual_data')]
)
def get_total_row(filtered_df):
    if filtered_df is None or len(filtered_df) == 0:
        return dash.no_update
    else:
        df_ = pd.DataFrame(filtered_df).mean(numeric_only=True).round(2)
        first_col = pd.DataFrame(data=['Mean', "Market"], index=['Ticker', "Market"])
        df_ = pd.concat([first_col, df_])
        columns = data_format_by_columns(list(df_.index))
        data = [{df_.index[i]: df_.iloc[i, 0] for i in range(len(df_.index))}]
        if data is None:
            return dash.no_update
        else:
            return columns, data


# COPY_TO_CLIPBOARD BUTTON
@app.callback(
    Output(component_id='confirm box', component_property='message'),
    Input(component_id='confirm box', component_property='submit_n_clicks'),
    State(component_id='data_table', component_property='derived_virtual_data')
)
def copy_to_clipboard(n_clicks, derived_virtual_data):
    if not n_clicks:
        return ''
    df_ = pd.DataFrame(derived_virtual_data)
    df_.to_clipboard(sep=',', index=False)
    return 'Copied to clipboard'


"""---------------------       SIDEBAR       -----------------------------"""


# SIDEBAR EXPAND AND COLLAPSE
@app.callback(
    [Output(component_id='sidebar', component_property='className'),
     Output(component_id='toggle_switch', component_property='children'),

     Output(component_id='option_sidebar', component_property='className'),
     Output(component_id='dividend_sidebar', component_property='className'),
     Output(component_id='analysis_report_sidebar', component_property='className'),
     Output(component_id='news_sidebar', component_property='className'),

     Output(component_id='optionbtn', component_property='className'),
     Output(component_id='dividendbtn', component_property='className'),
     Output(component_id='analysis_report_btn', component_property='className'),
     Output(component_id='news_btn', component_property='className')],

    [Input(component_id='optionbtn', component_property='n_clicks'),
     Input(component_id='dividendbtn', component_property='n_clicks'),
     Input(component_id='analysis_report_btn', component_property='n_clicks'),
     Input(component_id='news_btn', component_property='n_clicks'),
     Input(component_id='tabs', component_property='value')],

    [State(component_id="toggle_switch", component_property="children"),
     State(component_id='option_sidebar', component_property='className'),
     State(component_id='dividend_sidebar', component_property='className'),
     State(component_id='analysis_report_sidebar', component_property='className'),
     State(component_id='news_sidebar', component_property='className'),

     State(component_id='optionbtn', component_property='className'),
     State(component_id='dividendbtn', component_property='className'),
     State(component_id='analysis_report_btn', component_property='className'),
     State(component_id='news_btn', component_property='className')],
)
def show_hide_sidebar(option_clicks, dividend_click, analysis_click, news_click, tab_,
                      toggle_status, option_sidebar_class, dividend_sidebar_class, analysis_sidebar_class,
                      news_sidebar_class,
                      optionbtn_class, dividendbtn_class, analysisbtn_class, newsbtn_class):
    if tab_ == 'tab1' or tab_ == 'tab2':
        sidebar_classname = ''
    else:
        sidebar_classname = 'hide'
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if changed_id != '.':
        toggle_status.append(changed_id.replace(".n_clicks", ""))
    else:
        pass

    control = {
        'optionbtn': {
            'button_class': optionbtn_class,
            'sidebar_class': option_sidebar_class
        },
        'dividendbtn': {
            'button_class': dividendbtn_class,
            'sidebar_class': dividend_sidebar_class
        },
        'analysis_report_btn': {
            'button_class': analysisbtn_class,
            'sidebar_class': analysis_sidebar_class
        },
        'news_btn': {
            'button_class': newsbtn_class,
            'sidebar_class': news_sidebar_class
        }
    }

    _last = [b if b in changed_id else 'hide' for b in control.keys()]

    if len(toggle_status) == 0:
        return dash.no_update
    elif len(toggle_status) >= 2 and toggle_status[-1] == toggle_status[-2]:
        for i in range(len(list(control.keys()))):
            _key = list(control.keys())[i]
            toggle_status = []
            control[_key]['button_class'] = collapse(control[_key]['button_class'])
            control[_key]['sidebar_class'] = collapse(control[_key]['sidebar_class'])
    else:
        for i in range(len(list(control.keys()))):
            _key = list(control.keys())[i]
            if _last[i] == 'hide':
                control[_key]['button_class'] = collapse(control[_key]['button_class'])
                control[_key]['sidebar_class'] = collapse(control[_key]['sidebar_class'])
            else:
                control[_key]['button_class'] = expand(control[_key]['button_class'])
                control[_key]['sidebar_class'] = expand(control[_key]['sidebar_class'])
    return [sidebar_classname, toggle_status,
            control['optionbtn']['sidebar_class'],
            control['dividendbtn']['sidebar_class'],
            control['analysis_report_btn']['sidebar_class'],
            control['news_btn']['sidebar_class'],

            control['optionbtn']['button_class'],
            control['dividendbtn']['button_class'],
            control['analysis_report_btn']['button_class'],
            control['news_btn']['button_class'],
            ]


# SIDE BAR 1: GET NEWS ABOUT CURRENT TICKER
@app.callback(
    [Output(component_id="news_sidebar", component_property="children")],
    Input(component_id="news_btn", component_property="n_clicks"),
    [State(component_id='input_ticker', component_property='value'),
     State(component_id='toggle_switch', component_property='children')]
)
def update_news(n_clicks, ticker, toggle_status):
    # wireshark filter ip.addr == 45.124.85.161 and http
    try:
        ticker = ticker.upper()
    except AttributeError:
        raise PreventUpdate
    # Prevent update if already click news_btn
    try:
        if 'news_btn' in toggle_status:
            raise PreventUpdate
    except IndexError:
        pass

    if n_clicks is None:
        raise PreventUpdate
    else:
        result = NewsUpdater(ticker).run()
        if result.empty:
            return ["Không có tin tức cho mã này"]
        else:
            li = [
                html.Li(
                    children=[
                        html.A([result.iloc[i]],
                        id={'index': str(result.index[i]),'type':'news'},
                        target="_blank")]
                )
                for i in range(len(result.index))]
            return \
                [html.Ul(children=li, className='list-group')]


# SIDE BAR 1: GET NEWS LINK
@app.callback(
    Output(component_id={'index': MATCH,'type':'news'}, component_property='href'),
    Input(component_id={'index': MATCH,'type':'news'}, component_property='n_clicks'),
    State(component_id={'index': MATCH,'type':'news'}, component_property='children')
)
def get_link(__n_clicks, __date_title):
    if __n_clicks is None:
        raise PreventUpdate
    else:
        __title = re.sub("(.*\s{5})", "", str(__date_title))
        return list(search(__title, num_results=1))[0]



# SIDE BAR 2: GET ANALYSIS REPORT FOR CURRENT TICKER
@app.callback(
    [Output(component_id="analysis_report_sidebar", component_property="children")],
    Input(component_id="analysis_report_btn", component_property="n_clicks"),
    [State(component_id='input_ticker', component_property='value'),
     State(component_id='toggle_switch', component_property='children')]
)
def update_analysis_report(n_clicks, ticker, toggle_status):
    try:
        ticker = ticker.upper()
    except AttributeError:
        return dash.no_update
    # Prevent update if already click analysis_report_btn
    try:
        if 'analysis_report_btn' in toggle_status:
            raise PreventUpdate
    except IndexError:
        pass

    if n_clicks is None:
        return PreventUpdate
    else:
        result = AnalysisReportUpdater(ticker).run()
        if result.empty:
            return ["Không có báo cáo phân tích cho mã này"]
        else:
            li = []
            for i in range(len(result.index)):
                row = html.Li(
                    children=[
                        html.A(
                            children=[f'{result.iloc[i, 0]}     {result.iloc[i, 1]}     |     {result.iloc[i, 2]}'],
                            href = result.iloc[i,10],
                            target="_blank",
                            id={
                                'type': "analysisReport",
                                'index': str(result.index[i])
                            }
                        )
                    ],
                    className='list-group-item'
                )
                li.append(row)
            return \
                [html.Ul(children=li, className='list-group')]


'''# SIDE BAR 2: GET ANALYSIS LINK
@app.callback(
    Output(component_id={'type': 'analysisReport', 'index': MATCH}, component_property='href'),
    Input(component_id={'type': 'analysisReport', 'index': MATCH}, component_property='n_clicks'),
    State(component_id={'type': 'analysisReport', 'index': MATCH}, component_property='id')
)
def get_link(__n_clicks, __id):
    if __n_clicks is None:
        raise PreventUpdate
    else:
        _link = AnalysisReportUpdater('').get_analysis_report_link(__id)
        return _link
'''

# SIDE BAR 3: DISPLAY DIVIDEND HISTORY OF CURRENT TICKER
@app.callback(
    [Output(component_id="dividend_sidebar", component_property="children")],
    Input(component_id="dividendbtn", component_property="n_clicks"),
    [State(component_id='input_ticker', component_property='value'),
     State(component_id='toggle_switch', component_property='children')]
)
def update_dividend(n_clicks, ticker, toggle_status):
    try:
        ticker = ticker.upper()
    except AttributeError:
        return dash.no_update

    # Prevent update if already click dividendbtn
    try:
        if 'dividendbtn' in toggle_status:
            raise PreventUpdate
    except IndexError:
        pass

    if n_clicks is None:
        return PreventUpdate
    else:
        __df = dividend[dividend['Code'] == str(ticker).upper()].drop("Code", axis=1)
        __table = dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in __df.columns],
            data=__df.to_dict('records'),
            page_size=25,
            style_header={'backgroundColor': 'transparent'},
            style_cell={
                'backgroundColor': 'transparent',
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left',
                'font-family': "Times New Roman, Times, serif",
                'border': '1px solid rgb(58, 195, 214)'
            }
        )
        return [html.Div(
            children=[__table],
            style={"height": "70%"}
        )]


# SIDE BAR 3

# UPDATE DIVIDEND HISTORY OF CURRENT TICKER
# SIDE BAR 3

# UPDATE DIVIDEND HISTORY OF CURRENT TICKER
@app.callback(
    [Output(component_id="get_dividend_notification", component_property="is_open"),
     Output(component_id="get_dividend_notification", component_property="children")],
    [Input(component_id="get_dividend", component_property="n_clicks")]
)
def open_toast(n):
    if n:
        Dividend().run()
        return [True, "Finish on updating dividend data for all ticker"]
    else:
        return [False, ""]


# UPDATE FINANCE DATA OF CURRENT TICKER
@app.callback(
    [Output(component_id="update_individual_findata_notification", component_property="is_open"),
     Output(component_id="update_individual_findata_notification", component_property="children")],
    [Input(component_id="update_individual_findata", component_property="n_clicks")],
    [State(component_id='input_ticker', component_property='value')]
)
def open_toast(n, __ticker):
    if n:
        try:
            __ticker = __ticker.upper()
            DataUpdater(__ticker).update()
            Database('vietstock').update(__ticker)
            DerivationDatabase('vietstock').update(__ticker)
            return [True, f"Finish on updating individual financial data for {__ticker}"]
        except (KeyError, TypeError, AttributeError) as e:
            print(e)
            return [True, "No input ticker"]
    else:
        return [False, ""]


# UPDATE FINANCE DATA OF ENTIRE MARKET (NOT YET FUNCTIONED)
@app.callback(
    [Output(component_id="update_market_findata_notification", component_property="is_open"),
     Output(component_id="update_market_findata_notification", component_property="children")],
    [Input(component_id="update_market_findata", component_property="n_clicks")]
)
def open_toast(n):
    if n:
        return [True, "Finish on updating findata data for Entire market"]
    else:
        return [False, ""]


"""---------------------       TAB4       -----------------------------"""


# Update total Market Trading Overview pie chart
@app.callback(
    [Output('statistic_container', 'style'),
     Output('statistic_container', 'children'),
     ],
    Input('refresh_button', 'n_clicks'),
    State('market', 'value')
)
def update_market_over_view_charts(n_clicks, market):
    maximum_bar_number = 35
    try:
        if n_clicks is None:
            raise PreventUpdate
        else:
            show_charts = {'display': 'block'}

            # FETCH LIVE MARKET DATA
            # market_overview_data = pd.read_csv(market_overview_data_path, index_col=0)
            market_overview_data = GetMarketOverviewData(market).run()
            market_overview_data = market_overview_data[~market_overview_data['IndustryName2'].isna()]

            # Make charts
            market_overview_data['Info label'] = '<b>' + market_overview_data.index + '</b>' + '<br>' \
                                                 + market_overview_data['pricePercentChange'].astype(float).map(
                lambda n: '{:.2%}'.format(n)).astype(str)

            market_overview_data['index'] = '<b>' + market + '</b>'
            # market_overview_data = market_overview_data.sort_values(by=['capitalization'])

            # PLOTTING
            # OVERVIEW TREEMAP
            treemap = px.treemap(market_overview_data,
                                 path=['index', 'IndustryName2', 'Info label'],
                                 values='%Value',
                                 color='status',
                                 custom_data=['Name', 'pricePercentChange_52W'],
                                 color_discrete_map=get_color_discrete_map(market_overview_data),
                                 )
            treemap['data'][0].update(
                hovertemplate=
                '%{customdata[0]} <br>' +
                '%{label} <br>' +
                '52W change: %{customdata[1]:.2%}'

            )
            treemap.update_layout(
                margin=dict(t=20, l=0, r=0, b=0, pad=0),
                uniformtext=dict(minsize=10, mode='hide'),
                height=600

            )

            treemap.update_traces(
                marker_pad=dict(l=0.1, r=0.1, b=0.1),
                marker=dict(
                    line=dict(
                        color='#000000'
                    )
                ),
            )

            # FIG2
            # TOP TRADING COMPANY
            top_trading_companies = market_overview_data.sort_values('totalValue', ascending=False).head(
                maximum_bar_number)
            top_trading_companies_chart = go.Figure(
                data=[
                    go.Bar(
                        x=top_trading_companies['Info label'],
                        y=top_trading_companies['totalValue'],
                        marker_color=get_color_discrete_map(top_trading_companies, 'df')
                    ),
                    go.Scatter(
                        x=top_trading_companies['Info label'],
                        y=top_trading_companies['capitalization'],
                        yaxis='y2',
                        mode='markers',
                        marker=dict(size=12,
                                    line=dict(width=2,
                                              color='#6B6B61'),
                                    color='#FFFEE8'
                                    )
                    ),
                ],
                layout=go.Layout(
                    margin=dict(t=0, l=0, r=0, b=0, pad=0),
                    height=200,
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    uniformtext=dict(
                        minsize=12,
                        mode='show'
                    ),
                    xaxis=dict(
                        showgrid=False,
                        zeroline=False
                    ),
                    yaxis=dict(
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False
                    ),
                    yaxis2=dict(
                        overlaying='y',
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False
                    ),
                    barmode='group',
                )
            )

            # VERTICAL BAR CHART
            gr = market_overview_data.reset_index().groupby(['IndustryName2'])
            group_by_inds2 = pd.concat([
                pd.Series(data=gr.first().iloc[:, 0], name='ticker'),
                gr.sum()['totalValue'],
                pd.Series(data=gr.apply(lambda x: np.average(x['pricePercentChange'], weights=x['capitalization'])),
                          name='pricePercentChange')
            ], axis=1).sort_values(by=['totalValue'], ascending=True).tail(maximum_bar_number)

            vertical_bar_chart = go.Figure(
                data=[
                    go.Bar(
                        x=group_by_inds2['pricePercentChange'],
                        y=group_by_inds2.index,
                        orientation='h',
                        marker_color=get_color_discrete_map(group_by_inds2, 'list'),
                        marker=dict(line=dict(color='#000000')),
                        customdata=group_by_inds2['ticker'],
                        hovertemplate='%{y} <br> %{customdata}<extra></extra>'
                    ),
                    go.Scatter(
                        x=group_by_inds2['totalValue'],
                        y=group_by_inds2.index,
                        xaxis='x2',
                        mode='lines',
                        opacity=0.5,
                        line=dict(color='#ad7878')
                    )
                ],
                layout=go.Layout(
                    autosize=False,
                    height=850,
                    width=300,
                    margin=dict(
                        t=0, l=0, r=0, b=20, pad=0, autoexpand=False
                    ),
                    plot_bgcolor='white',
                    showlegend=False,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='#e8e8e8',
                        tickformat=',.0%',
                        title=None,
                        dtick=0.01,

                    ),
                    yaxis=dict(
                        title=None,
                        showgrid=False,
                    ),
                    xaxis2=dict(
                        overlaying='x',
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False
                    ),
                )
            )
            for i in range(len(group_by_inds2.index)):
                vertical_bar_chart.add_annotation(dict(
                    font=dict(color='#6b6b6b'),
                    x=0,
                    y=group_by_inds2.index[i],
                    showarrow=False,
                    text=str(group_by_inds2.index[i]),
                    textangle=0,
                    xanchor='left',
                    xref='paper',
                    yref="y"),
                    width=300,
                    align='left',
                )

            charts = \
                [
                    html.Div([
                        dcc.Graph(
                            figure=vertical_bar_chart,
                            config={'displayModeBar': False})
                    ], className='two columns'),
                    html.Div([
                        html.Div(
                            [dcc.Graph(figure=top_trading_companies_chart,
                                       config={'displayModeBar': False}
                                       )]),
                        html.Div([dcc.Graph(figure=treemap)])
                    ], className='ten columns')
                ]
            return [show_charts, charts]
    except IndexError:
        raise PreventUpdate


app.config['suppress_callback_exceptions'] = True

if __name__ == '__main__':
    app.run_server(debug=True)  # debug=True

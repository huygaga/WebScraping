import pandas as pd
import Support_function as Sf
from plotly.subplots import make_subplots
from Setup import root
from Layout import traces
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from time import time

sorted_by = 'Sales'
compare_unit = 20
general_info = pd.read_csv(root.loc['General info', 'Path'], index_col=0)
derivation_database = pd.read_csv(root.loc['cophieu68_derivation', 'Path'], index_col=[0, 1])
quarter = derivation_database.filter(regex='^Q').dropna(how='all', axis=0).dropna(how='all', axis=1)
annual = derivation_database.filter(regex='^Y').dropna(how='all', axis=0).dropna(how='all', axis=1)


def get_similar_company(ticker):
    info = list(general_info.xs(ticker)[2:4])
    df = general_info[general_info['Ngành cấp 2'].isin(info) | general_info['Ngành cấp 3'].isin(info)]
    df = df.loc[~df.index.duplicated(keep='first')]
    return df


def get_similar_company_data(temporal_database, ticker):
    similar_tickers = get_similar_company(ticker)
    similar_data = temporal_database[temporal_database.index.get_level_values(0).isin(similar_tickers.index)].dropna(
        how='all', axis=1)
    most_recent = similar_data.columns[1]
    temp = similar_data[similar_data.index.get_level_values(1) == sorted_by].sort_values(most_recent, ascending=False)
    sorted_index = Sf.shift_to_top(list(temp.index.get_level_values(0)), ticker)
    similar_data = similar_data.reindex(sorted_index, level=0)
    return similar_data


def shrink_dataframe(_similardata, _size):
    shrinked = _similardata.loc[_similardata.index.get_level_values(0).unique()[:_size].tolist()].dropna(how='all',
                                                                                                         axis=1)
    return shrinked

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    #'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#2980b9',
    'color': 'white',
    'padding': '6px'
}


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# ['https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css']
# ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = \
    html.Div(children=[
        # HEADER
        html.Div(
            children=[
                html.Div(
                    className='three columns', style={'height': '100%', 'text-align': 'middle'},
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
                        ),
                    ]
                ),
                html.Div(
                    id='ticker_name',
                    className='three columns', style={'height': '100%', 'vertical-align':'middle', 'overflow-wrap': 'break-word'},
                ),
                html.Div(
                    id='ticker_properties',
                    className='six columns', style={'height': '100%'},
                ),
        ]),
        # PLOTTING AREA
        html.Div(
            className='twelve columns',
            children=[
                dcc.Tabs([
                    dcc.Tab(
                        id='tab1',
                        label='Financial Report',
                        children=[
                            dcc.Graph(
                                id='graph1',
                                style={'height': 800}
                            ),
                        ],
                        style=tab_style,
                        selected_style=tab_selected_style
                    ),
                    dcc.Tab(
                        id='tab2',
                        label='Comparison',
                        children=[
                            html.P([
                                html.Label("Time Period"),
                                html.Div(id='slider_tab2'),
                                html.Div(id='updatemode-output-container', style={'margin-top': 20})
                            ]),
                            dcc.Graph(
                                id='graph2',
                                style={'height': 800}
                            ),
                            html.Div(id='intermediate-value', style={'display': 'none'})
                        ],
                        style=tab_style,
                        selected_style=tab_selected_style
                    )
                ], style=tabs_styles)
        ])
    ])


# TO UPDATE TICKER FULL NAME
@app.callback(
    Output(component_id='ticker_name', component_property='children'),
    [Input(component_id='input_ticker', component_property='value')])
def update_title(input_):
    try:
        if len(input_) == 3:
            input_ = input_.upper()
            ticker_info = general_info.loc[input_, :]
            return [html.H1(style={'margin':'2rem 0 0 0', 'color': 'rgb(38 114 165)'},children=input_),
                    html.H3(style={'font-style': 'regular', 'margin': '0.1rem 0rem 0rem 0rem'}, children=[ticker_info['Tên công ty']])]
    except (KeyError, TypeError):
        return ""


@app.callback(
    Output(component_id='ticker_properties', component_property='children'),
    [Input(component_id='input_ticker', component_property='value')])
def update_properties(input_):
    try:
        if len(input_) == 3:
            input_ = input_.upper()
            ticker_info = general_info.loc[input_, :]
            return \
                [html.Table([
                    html.Tr([
                        html.Td('Ngành cấp 1'),html.Td(ticker_info['Ngành cấp 1']),
                        html.Td('Sàn'),html.Td(ticker_info['Sàn']),
                    ]),
                    html.Tr([
                        html.Td('Ngành cấp 2'),html.Td(ticker_info['Ngành cấp 2']),
                        html.Td('Ngày GDĐT'),html.Td(ticker_info['Ngày GDĐT']),
                    ]),
                    html.Tr([
                        html.Td('Ngành cấp 3'),html.Td(ticker_info['Ngành cấp 3']),
                        html.Td('Khối lượng NY/ĐKGD'),html.Td(ticker_info['Khối lượng NY/ĐKGD']),
                    ])
                ], style={'width':'100%'})]
    except (KeyError, TypeError):
        return ""


# GET DATABASE:
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
            similar_data.to_csv(root.loc['temp_', 'Path'], encoding="utf-8-sig")
            return ticker
    except (KeyError, TypeError):
        pass


@app.callback(
    Output(component_id='slider_tab2', component_property='children'),
    [Input(component_id='intermediate-value', component_property='children')]
)
def make_slider_properties(_input):
    _mark_label = pd.read_csv(root.loc['temp_', 'Path'], index_col=[0,1]).columns
    _mark = {i: _mark_label[i] for i in range(len(_mark_label))}
    _min = 0
    _max = len(_mark_label)
    return dcc.Slider(id='time_slider',
                        marks=_mark,
                        min=_min,
                        max=_max,
                        value=1)


# TO UPDATE FIGRUES AT TAB1
@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='intermediate-value', component_property='children')]
)
def update_graph(text):
    ticker = text
    fig1 = make_subplots(
        rows=3, cols=1,
        vertical_spacing=0.01,
        row_heights=[0.4, 0.4, 0.2],
        shared_xaxes=True,
        specs=[[{'secondary_y': True}], [{'secondary_y': True}], [{'secondary_y': True}]],
        subplot_titles=(" ", " ")
    )

    similar_data = pd.read_csv(root.loc['temp_', 'Path'],index_col=[0,1])

    # GET PLOT DATA
    to_plot_tab1 = shrink_dataframe(similar_data, 1)
    x1 = to_plot_tab1.columns
    for key in traces.keys():
        y1 = to_plot_tab1.loc[(ticker, traces[key]['name']), :]
        fig1.add_trace(Sf.trace_data(traces[key], x1, y1),
                       secondary_y=traces[key]['secondary_y'],
                       row=traces[key]['row'], col=traces[key]['col'])

    zeroline_color = 'rgb( 146, 43, 33 )'
    fig1.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(
            family='Times New Roman',
            color='#7f7f7f'
        ),
        xaxis=dict(
            showgrid=True,
        ),
        xaxis2=dict(
            showgrid=True,
        ),
        yaxis2=dict(
            showgrid=False,
            tickformat=".2%",
            zeroline=True,
            zerolinecolor=zeroline_color
        ),
        yaxis4=dict(
            showgrid=False,
            tickformat=".0%",
            side='right',
        ),
    )
    return fig1

# TO UPDATE FIGRUES AT TAB2
@app.callback(
    Output(component_id='graph2', component_property='figure'),
    [Input(component_id='intermediate-value', component_property='children'),
    Input(component_id='time_slider', component_property='value')]
)
def update_graph(text,value):
    fig2 = make_subplots(
        rows=3, cols=1,
        vertical_spacing=0.01,
        row_heights=[0.4, 0.4, 0.2],
        shared_xaxes=True,
        specs=[[{'secondary_y': True}], [{'secondary_y': True}], [{'secondary_y': True}]],
        subplot_titles=(" ", " ")
    )
    similar_data = pd.read_csv(root.loc['temp_', 'Path'],index_col=[0,1])

    # GET PLOT DATA
    to_plot_tab2 = shrink_dataframe(similar_data, compare_unit)
    shrink_indexes = to_plot_tab2.index.get_level_values(0).drop_duplicates(keep='first')
    x2 = [i + '<br>' + general_info.loc[i, 'Tên công ty'] for i in shrink_indexes]
    for key in traces.keys():
        y2 = to_plot_tab2[to_plot_tab2.index.get_level_values(1) == traces[key]['name']].iloc[:,value]
        fig2.add_trace(Sf.trace_data(traces[key], x2, y2),
                       secondary_y=traces[key]['secondary_y'],
                       row=traces[key]['row'], col=traces[key]['col'])

    zeroline_color = 'rgb( 146, 43, 33 )'
    fig2.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(
            family='Times New Roman',
            color='#7f7f7f'
        ),
        xaxis=dict(
            showgrid=True,
        ),
        xaxis2=dict(
            showgrid=True,
        ),
        yaxis2=dict(
            showgrid=False,
            tickformat=".2%"
        ),
        yaxis4=dict(
            showgrid=False,
            tickformat=".0%",
            side='right',
        ),
    )
    fig2.update_traces(mode='lines+markers',line=dict(width=1),
                       selector=dict(type='scatter'))
    return fig2


'''@app.callback(
    [Output(component_id='time_slider', component_property='max'),
     Output(component_id='time_slider', component_property='mark')],
    [Input(component_id='time_slider', component_property='value')]
)
def silder(value):
    return value+10, {i : i for i in range(0, value)}'''


if __name__ == '__main__':
    app.run_server(debug=True)  # debug=True


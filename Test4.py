from Controller import *
def get_info_tooltip2(df_):
    temp2 = pd.DataFrame()
    temp_ = info[info['Ticker'].isin(list(df_['Ticker']))]
    temp2['Ticker'] = temp_['Ticker'] + ' - ' + temp_['Name']
    return [
        {
            k:
                {'type': 'text', 'value': str(v)} for k, v in row.items()
        } for row in temp2[['Ticker']].to_dict('records')
    ]
def test():
    table = get_statistic_table("Q2 2022")
    ticker = ['VNM','HPG']
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

    tooltip_data_ = get_info_tooltip2(table)

    columns = data_format_by_columns(list(table.columns))
    data = table.to_dict('records')
    print(tooltip_data_)
test()
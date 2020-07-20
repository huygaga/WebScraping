import Support_function as Sf
from plotly.subplots import make_subplots



color = dict(
    blue='rgb(41,128,185)',
    dark_blue='rgb(13, 74, 115)',
    green='rgb(39,174,96)',
    dark_green='rgb(78, 148, 108)',
    orange='rgb(230,126,34)',
    light_brownish_orange='rgb(242,191,135)',
    yellow='rgb(232, 214, 51)',
    dark_pink='rgb(187,89,99)',
    black='rgb(0,0,0)',
)

traces = {
    'trace1': {
        'name': 'Sales', 'look_up_name': 'Doanh Thu Thuần',
        'type': 'bar',
        'secondary_y': None,'row': 1, 'col': 1,
        'marker color':Sf.marker_control(color['blue']),},
    'trace2': {
        'name': 'Gross profit', 'look_up_name': 'Lợi Nhuận Gộp',
        'type': 'bar',
        'secondary_y': None, 'row': 1, 'col': 1,
        'marker color':Sf.marker_control(color['green']),},
    'trace3': {
        'name': 'Net profit', 'look_up_name': 'Lợi nhuận sau thuế thu nhập doanh nghiệp',
        'type': 'bar',
        'secondary_y': None,'row': 1, 'col': 1,
        'marker color':Sf.marker_control(color['orange']),},
    'trace4': {
        'name': 'Total assets', 'look_up_name': 'TỔNG TÀI SẢN',
        'type': 'bar',
        'secondary_y': None, 'row': 2, 'col': 1,
        'marker color':Sf.marker_control(color['light_brownish_orange']),},
    'trace5': {
        'name': 'Equity', 'look_up_name': 'Vốn chủ sở hữu',
        'type': 'bar',
        'secondary_y': None, 'row': 2, 'col': 1,
        'marker color':Sf.marker_control(color['dark_green']),},
    'trace6': {
        'name': 'Total debt', 'look_up_name': 'Tổng Nợ',
        'type': 'bar',
        'secondary_y': None, 'row': 2, 'col': 1,
        'marker color': Sf.marker_control(color['dark_pink']),},
    'trace7': {
        'name': 'Profit Margin', 'look_up_name': 'Lợi nhuận sau thuế thu nhập doanh nghiệp/Doanh Thu Thuần',
        'type': 'scatter',
        'secondary_y': True,'row': 1, 'col': 1,
        'marker color': Sf.marker_control(color['dark_pink']),},
    'trace8': {
        'type': 'scatter',
        'name': 'ROE', 'look_up_name': 'Lợi nhuận sau thuế thu nhập doanh nghiệp/Vốn chủ sở hữu',
        'secondary_y': True, 'row': 2, 'col': 1,
        'marker color': Sf.marker_control(color['black']),},
    'trace9': {
        'type': 'scatter',
        'name': 'ROA', 'look_up_name': 'Lợi nhuận sau thuế thu nhập doanh nghiệp/TỔNG TÀI SẢN',
        'secondary_y': True, 'row': 2, 'col': 1,
        'marker color': Sf.marker_control(color['dark_blue']),},
    'trace11': {
        'type': 'scatter',
        'name': 'AGR Sales', 'look_up_name': 'Doanh Thu Thuần',
        'secondary_y': True, 'row': 1, 'col': 1,
        'marker color': Sf.marker_control(color['blue']),},
    'trace12': {
        'type': 'scatter',
        'name': 'AGR Net Profit', 'look_up_name': 'Lợi nhuận sau thuế thu nhập doanh nghiệp',
        'secondary_y': True, 'row': 1, 'col': 1,
        'marker color': Sf.marker_control(color['orange']),},
    'trace13': {
        'type': 'scatter',
        'name': 'Equity Multiplier', 'look_up_name': 'Vốn chủ sở hữu/TỔNG TÀI SẢN',
        'secondary_y': True, 'row': 2, 'col': 1,
        'marker color': Sf.marker_control(color['dark_pink']),},
    'trace14': {
        'type': 'scatter',
        'name': 'EPS', 'look_up_name': 'EPS(EPS chưa điều chỉnh)',
        'secondary_y': None, 'row': 3, 'col': 1,
        'marker color': Sf.marker_control(color['blue']),},
    'trace15': {
        'type': 'scatter',
        'name': 'P/E', 'look_up_name': 'PE',
        'secondary_y': True, 'row': 3, 'col': 1,
        'marker color': Sf.marker_control(color['dark_pink']),},
    'trace16': {
        'type': 'scatter',
        'name': 'P/B', 'look_up_name': 'Giá Cuối Kỳ/Giá Sổ Sách',
        'secondary_y': True, 'row': 3, 'col': 1,
        'marker color': Sf.marker_control(color['dark_green']),},
}


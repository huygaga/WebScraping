from Setup import root
import pandas as pd
import Support_function as Sf
key=('Doanh Thu Thuần','Lợi nhuận sau thuế thu nhập doanh nghiệp','TỔNG TÀI SẢN','Vốn chủ sở hữu')
date = ['Q4 2019']
filter = pd.DataFrame()
for i in range(len(root)):
    pat = root.iloc[i, 0]
    stic = root.index[i]
    try:
        cols = pd.read_csv(pat, nrows=1).columns
        df = pd.read_csv(pat, usecols=cols[2:], index_col=cols[2])
        ext = pd.DataFrame(df.loc[key, 'Q4 2019'])
        ext.columns = [stic]
        trans_ = ext.transpose()
        filter = filter.append(trans_)
    except (IndexError,KeyError) as e:
        print(stic)
filter.to_csv('D:/Filter.csv',encoding='utf-8-sig')





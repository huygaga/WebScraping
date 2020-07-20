from selenium import webdriver
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

page = 'https://www.worldometers.info/coronavirus/'
saving_path = 'C:/Users/anhbui/Desktop/New Folder/corona.csv'


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

class Crawl:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def get_table_id(self):
        tables = self.driver.find_elements_by_tag_name('table')
        for table in tables:
            if 'today' in table.get_attribute('id'):
                return table.get_attribute('id')

    def get_content(self, sup_xpath, sub_xpath):
        content = []
        super_ = self.driver.find_elements_by_xpath(sup_xpath)
        if len(super_) > 1:
            for sup in super_:
                content.append([sub.text for sub in sup.find_elements_by_xpath(sub_xpath)])
        else:
            content = [sub.text for sub in self.driver.find_element_by_xpath(sup_xpath).find_elements_by_xpath(sub_xpath)]
        return content

    def crawl(self):
        self.driver.get(self.url)
        table_id = self.get_table_id()
        rows_xpath = '{}{}{}'.format('//*[@id="', table_id, '"]/tbody[1]/tr')
        heading_xpath = '{}{}{}'.format('//*[@id="', table_id, '"]/thead/tr')

        headers = self.get_content(heading_xpath, 'th')
        data = self.get_content(rows_xpath, 'td')

        dict_ = {}
        for h in range(len(headers)):
            dict_[headers[h]] = [data[i][h] for i in range(len(data))]
        df = pd.DataFrame(dict_)
        df.to_csv(saving_path, index=False)


class Visualization:
    def __init__(self, path, range_):
        self.path = path
        self.df = pd.read_csv(self.path, thousands= r',')
        self.range_ = range_
    def print_text(self):
        print("Total cases worldwide: " + str(self.df.sum()[1]) + '\n')
        for i in range(len(self.df.iloc[:, 0])):
            if self.df.iloc[i, 0] == "Vietnam":
                print('Total case in Viet Nam: ' + str(self.df.iloc[i, 1]) + ' at rank: ' + str(i) + " world wide")
                print('Total case/ 1 Mil population in Viet Nam: ' + str(self.df.iloc[i, 8]) + '\n')
        print(self.df)

    def report(self):
        self.print_text()
        self.df.fillna(0, inplace=True)
        to_plot = self.df[:self.range_][:]
        stacked = 0
        fig, ax = plt.subplots()

        plt.xticks(rotation=90)
        for name in to_plot:
            if to_plot.columns.get_loc(name) in [3,5,6]:
                ax.bar(to_plot.iloc[:, 0], to_plot[name].values, bottom=stacked, label=name)
                stacked += to_plot[name].values
        death_ratio = to_plot.iloc[:, 3]*100/stacked

        recover_ratio = to_plot.iloc[:, 5]*100/stacked
        ax2 = ax.twinx()
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax2.plot(to_plot.iloc[:, 0], death_ratio, color ='red', LineWidth=0.4, label = 'Death Ratio')
        #ax2.plot(to_plot.iloc[:, 0], recover_ratio, color='green', label='Recover Ratio')


        ax.legend()
        plt.show()
        plt.savefig('C:/Users/anhbui/Desktop/New Folder/corona.png')

#crawl = Crawl(page).crawl()

Visualization(saving_path, range_ =20).report()



















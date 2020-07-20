import pandas as pd
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import sys
from Setup import root
from random import randint
# MISSING HEADER WHEN CLICK PREVIOUS BUTTON
barn_path = 'D:/Barn/Financial data/vietstock/'
class New_Crawl():
    def __init__(self, ticker_):
        self.ticker = ticker_
        self.url = '{}{}{}'.format('https://finance.vietstock.vn/', self.ticker.upper(), '/tai-chinh.htm')
        self.tables_selector = 'div.table-responsive.m-b'
        self.headings_selector = 'th.text-center.col-90>b'
        self.previous_button_selector = 'div[name="btn-page-2"].btn.btn-default.m-l'
        self.pull_right_button_selector = 'div[name="btn-page-4"].btn.btn-default.m-l'
        self.period_selector = 'select[name="period"].form-control'
        self.confirm_period_button = 'button[type="button"].btn.bg.m-l'
        self.driver = self.get_driver()

    def get_driver(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)
        try:
            WebDriverWait(driver, 20).until(lambda x: x.find_elements_by_tag_name(self.tables_selector))
            print("Done preparation for " + self.ticker)
        except exceptions.TimeoutException:
            print("Error: Loading time out when prepare for "+self.ticker)
            return None
        return driver

    def click_previous_button(self):
        disabled = self.previous_button_selector + '.disabled'
        if self.driver.find_elements_by_css_selector(disabled):
            return False
        else:
            WebDriverWait(self.driver, 5).\
                until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.previous_button_selector))).click()
            return True

    def switch_period(self):
        current = self.driver.find_element_by_css_selector(self.period_selector).get_attribute('value')
        if current == '1':
            switch = '2'
        else:
            switch = '1'
        select = Select(self.driver.find_element_by_css_selector(self.period_selector))
        select.select_by_value(switch)
        self.driver.find_element_by_css_selector(self.confirm_period_button).click()
        print("Period switched.")
        time.sleep(3)

    def get_column_headers(self):
        table = self.driver.find_element_by_css_selector(self.tables_selector)
        headings = table.find_elements_by_css_selector(self.headings_selector)
        columns = [heading.text for heading in headings]
        return columns

    def crawl_unit(self):
        df = pd.DataFrame()
        WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'th.text-center.col-90')))
        tables = self.driver.find_elements_by_css_selector(self.tables_selector)
        for table in tables:
            rows = table.find_elements_by_tag_name('tr')
            for row in rows[1:]:
                try:
                    row_index = row.find_element_by_tag_name('td')
                    cells = row.find_elements_by_css_selector('td.text-right')
                    ser = pd.Series(data=[cell.text for cell in cells], name=row_index.text)
                    df = df.append(ser)
                except TypeError as e:
                    print(e)
        df.columns = self.get_column_headers()
        return df

    def crawl_one_period(self):
        current = self.driver.find_element_by_css_selector(self.period_selector).get_attribute('value')
        if current == '1':
            current_period = 'Annual'
        else:
            current_period = 'Quarterly'
        df = pd.DataFrame()
        while True:
            crawl_unit = self.crawl_unit()
            df = pd.concat([df, crawl_unit], axis=1)
            if self.click_previous_button():
                self.click_previous_button()
            else:
                break
        df.to_csv(barn_path+current_period+'/'+self.ticker+'.csv', encoding='utf-8-sig')
        return df

    def run(self):
        self.crawl_one_period()
        # Pull-right fist before switch
        self.driver.find_element_by_css_selector(self.pull_right_button_selector).click()
        time.sleep(3)
        self.switch_period()
        self.crawl_one_period()
        print(self.crawl_one_period())
        self.driver.quit()
        print('Finish crawling on '+self.ticker)


crawl = New_Crawl('AAA')
crawl.run()

'''crawl_list = list(root.index[~(root.index.str.len()!=3)])


def get_index(ticker):
    for i in range(len(crawl_list)):
        if crawl_list[i] == ticker:
            print(i)
            return i

def run(list_):
    for i in list_:
        time.sleep(randint(5,20))
        try:
            crawl = New_Crawl(i)
            crawl.run()
            text = 'i'
        except:
            text = 'Error at '+i+' with code '+str(sys.exc_info()[0])
            print(text)
            continue'''













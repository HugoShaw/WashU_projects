# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 22:48:54 2021

@author: Hugo Xue
"""

'''用selenium在京东上搜索避孕套，并将搜索结果的二级页面链接给爬下来'''

from selenium import webdriver
import time
import openpyxl

class JDSpider(object):
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.url = 'https://www.jd.com/'
        self.i = 0
        
    # 获取搜索页面
    def get_page(self):
        self.browser.get(self.url)
        self.browser.find_element_by_xpath('//*[@id="key"]').send_keys('避孕套')
        self.browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
        # 留出时间给页面加载
        time.sleep(10)

    # 解析页面
    def parse_page(self):
        # 把进度条拉到最下面
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        time.sleep(15)

        products_list = []
        li_list = self.browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
        for li in li_list:
            price = li.find_element_by_xpath(
                './div/div[@class="p-price"]/strong/i').text.strip()
            product_name = li.find_element_by_xpath(
                './div/div[@class="p-name p-name-type-2"]/a/em').text.strip()
            link = li.find_element_by_xpath(
                './div/div[3]/a').get_attribute('href')
            products_list.append([price,product_name,link])
            
            self.i += 1
            
        self.save_page(products_list)
        
    def save_page(self,products_list):
        products_list = products_list
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = 'jd_prod' 
        sheet['A1'] = 'price'
        sheet['B1'] = 'product_name'
        sheet['C1'] = 'link'

        for product in products_list:
            sheet.append(product)
            
        filename = 'products-{}.xlsx'.format(self.i)
        wb.save(filename)

    def main(self):
        self.get_page()
        while True:
            self.parse_page()
            # 判断是否为最后1页
            # 不是最后1页,点击下一页
            if self.browser.page_source.find('下一页') != -1:
                # 不是最后1页,找到下一页按钮
                self.browser.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]/em').click()
                time.sleep(30)
            else:
                break
        print(self.i)

if __name__ == '__main__':
    spider = JDSpider()
    spider.main()
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 22:52:55 2021

@author: Hugo Xue
"""

'''
利用抓取到的二级页面链接，进行二级页面的内容抓取，将抓取到的数据存入excel，以防
程序中断，将每一个产品抓取到的内容都进行一次保存，保存到excel
'''

from selenium import webdriver
import time
import openpyxl
import pandas as pd

data = pd.read_excel('product_links.xlsx')
links = data.link

class JD2(object):
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.i = 1963

    # 获取响应
    def get_page(self,url):
        self.browser.get(url)
        # 直接调用解析函数
        time.sleep(2)
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        time.sleep(2)

    # 解析
    def parse_page(self):
        contents_list = []
        
        try:
            name = self.browser.find_element_by_xpath(
                '//div[@class="sku-name"]').text.strip()
        except:
            name =""
        contents_list.append(name)
        
        try:
            price = self.browser.find_element_by_xpath(
                '//span[@class="p-price"]').text.strip()
        except:
            price = ""
        contents_list.append(price)
        
        try:
            percent_pro = self.browser.find_element_by_xpath(
                '//*[@id="comment"]/div[@class="mc"]/div[1]/div[1]').text.strip()
        except:
            percent_pro = ''
        contents_list.append(percent_pro)
        try:
            percent_info = self.browser.find_element_by_xpath(
                '//*[@id="comment"]/div[@class="mc"]/div[1]/div[2]').text.strip()
        except:
            percent_info = ''
        contents_list.append(percent_info)
        try:
            all_comment = self.browser.find_element_by_xpath(
                '//*[@id="comment"]/div[@class="mc"]/div[2]/div/ul/li/a').text.strip()
        except:
            all_comment = ''
        contents_list.append(all_comment)
        try:
            pic_comment = self.browser.find_element_by_xpath(
                '//*[@id="comment"]/div[@class="mc"]/div[2]/div/ul/li[2]/a').text.strip()
        except:
            pic_comment = ''
        contents_list.append(pic_comment)
        try:
            vid_comment = self.browser.find_element_by_xpath(
                '//*[@id="comment"]/div[@class="mc"]/div[2]/div/ul/li[3]/a').text.strip()
        except:
            vid_comment = ''
        contents_list.append(vid_comment)
        try:
            add_comment = self.browser.find_element_by_xpath(
                '//*[@id="comment"]/div[@class="mc"]/div[2]/div/ul/li[4]/a').text.strip()
        except:
            add_comment = ''
        contents_list.append(add_comment)
        try:
            pro_comment = self.browser.find_element_by_xpath(
                '//*[@id="comment"]/div[@class="mc"]/div[2]/div/ul/li[5]/a').text.strip()
        except:
            pro_comment = ''
        contents_list.append(pro_comment)
        try:
            mid_comment = self.browser.find_element_by_xpath(
                '//*[@id="comment"]/div[@class="mc"]/div[2]/div/ul/li[6]/a').text.strip()
        except:
            mid_comment = ''
        contents_list.append(mid_comment)
        try:
            con_comment = self.browser.find_element_by_xpath(
                '//*[@id="comment"]/div[@class="mc"]/div[2]/div/ul/li[7]/a').text.strip()
        except:
            con_comment = ''
        contents_list.append(con_comment)
                
        # good comments
        try:
            self.browser.find_element_by_xpath('//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[5]/a').click()
            time.sleep(2)
            
            pro_com_list = []
            com = self.browser.find_elements_by_xpath(
                '//p[@class="comment-con"]')
            
            for p in com:
                p_txt = p.text.strip()
                pro_com_list.append(p_txt)
                
            pro_comments = " ".join(pro_com_list)
        except:
            pro_comments = ''
        contents_list.append(pro_comments)
        
        # add comments
        try:
            self.browser.find_element_by_xpath('//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[4]/a').click()
            time.sleep(2)
            
            add_com_list = []
            add_com = self.browser.find_elements_by_xpath(
                '//p[@class="comment-con"]')
            
            for p in add_com:
                p_txt = p.text.strip()
                add_com_list.append(p_txt)
            
            add_comments = " ".join(add_com_list)
        except:
            add_comments = ''
        contents_list.append(add_comments)
        
        # mid comments
        try:
            self.browser.find_element_by_xpath('//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[6]').click()
            time.sleep(1)
        
            
            mid_com_list = []
            mid_com = self.browser.find_elements_by_xpath(
                '//p[@class="comment-con"]')
            
            for p in mid_com:
                p_txt = p.text.strip()
                mid_com_list.append(p_txt)
            
            mid_comments = " ".join(mid_com_list)
        except:
            mid_comments = ''
        contents_list.append(mid_comments)
        
        # con comments
        try:
            self.browser.find_element_by_xpath('//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[7]').click()
            time.sleep(1)
            
            con_com_list = []
            con_com = self.browser.find_elements_by_xpath(
                '//p[@class="comment-con"]')
            
            for p in con_com:
                p_txt = p.text.strip()
                con_com_list.append(p_txt)
            
            con_comments = " ".join(con_com_list)       
        except:
            con_comments = ''
        contents_list.append(con_comments)
        
        self.i += 1
            
        self.save_page(contents_list)
        
    def save_page(self,contents_list):
        contents_list = contents_list
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = 'jd_prods' 
        sheet['A1'] = 'name'
        sheet['B1'] = 'price'
        sheet['C1'] = 'percent_pro'
        sheet['D1'] = 'percent_info'
        sheet['E1'] = 'all_comment'
        sheet['F1'] = 'pic_comment'
        sheet['G1'] = 'vid_comment'
        sheet['H1'] = 'add_comment'
        sheet['I1'] = 'pro_comment'
        sheet['J1'] = 'mid_comment'
        sheet['K1'] = 'con_comment'
        sheet['L1'] = 'pro_comments'
        sheet['M1'] = 'add_comments'
        sheet['N1'] = 'mid_comments'
        sheet['O1'] = 'con_comments'

        sheet.append(contents_list)
            
        filename = 'products-{}.xlsx'.format(self.i)
        wb.save(filename)


    def main(self):
        for link in links[1964:]:
            self.get_page(url=link)
            self.parse_page()
            
if __name__ == '__main__':
    sd = JD2()
    sd.main()

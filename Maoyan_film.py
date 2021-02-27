# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 17:11:43 2021

@author: Hugo Xue
@email: hugo@wustl.edu

"""
from urllib import request, parse
import time
import random 
import re
import csv

class MaoyanSpider(object):
    def __init__(self):
        # initialize your target website
        self.url = 'https://maoyan.com/board/4?offset={}'
        # initialize your headers
        self.headers = {'User-Agent':'Mozilla/5.0'}

    # get your response
    def get_page(self,url):
        req = request.Request(url=url,headers=self.headers)
        res = request.urlopen(req)
        # decode your response to get your html content
        html = res.read().decode('utf-8')
        # use parse_page()
        self.parse_page(html)
    
    # parse your page
    def parse_page(self,html):
        # use re package to greedy search the data you want 
        x = '<div class="movie-item-info">.*?title="(.*?)".*?class="star">(.*?)</p>.*?releasetime">(.*?)</p>'
        pattern = re.compile(x,re.S)
        # store data into a list
        r_list = pattern.findall(html)
        # try to save your data
        self.write_page(r_list)

    # save your data into csv file
    def write_page(self,r_list):
        film_list = []
        with open('maoyan.csv','a',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            for r in r_list:
                t = (r[0].strip(), r[1].strip(), r[2].strip()[5:15])
                film_list.append(t)
                
            writer.writerows(film_list)
             
    # main
    def main(self):
        start = int(input('input your start page: '))
        end = int(input('input your ending page: '))
        
        # get your pages
        for page in range(start, end+1):
            offset = (page-1)*10
            url = self.url.format(offset)
            
            # get your data
            self.get_page(url)
            
            # prompt
            print('The {} page completed!'.format(page))
        
            # control you crawling speed
            time.sleep(random.randint(1,3))
        
        
if __name__ == '__main__':
    start = time.time()
    spider = MaoyanSpider()
    spider.main()    
    end = time.time()
    print('execute time: %.2f' % (end-start)) 



























# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 22:55:55 2021

@author: Hugo Xue
"""

'''合并二级页面抓取到的每个产品数据的excel文件，合并成一个文件'''
import glob
import os
import pandas as pd
class MergeExcel(object):
    def __init__(self, headers):
        # 需要提取的列名
        self.headers = headers
        # 创建一个数据空间用于存储数据
        self.datas = pd.DataFrame(columns=self.headers)

    def get_file_path(self, dir_path):
        # 递归获取所有excel文件
        file_paths = glob.glob(dir_path + '/' + '*.xlsx*', recursive=True)
        return file_paths

    def merge_excel(self, file_path):
        # 读取、合并文件
        data = pd.read_excel(file_path)
        self.datas = self.datas.append(data[self.headers])

    def run(self):
        # 获取当前文件夹名称
        # dir_path = os.path.dirname(__file__)
        dir_path = os.getcwd()

        # 获取所有excel文件路径
        file_paths = self.get_file_path(dir_path)
        # print(file_paths)

        # 遍历所有的excel文件路径
        for file_path in file_paths:
            self.merge_excel(file_path)
            print(file_path.split('\\')[-1], '已合并')

        # 保存
        self.datas.to_excel('products.xlsx', sheet_name='Sheet1', index=False, header=True)

if __name__ == '__main__':
    # 输入需要提取的列名
    heads = [
        'name',
        'price',
        'percent_pro',
        'all_comment',
        'pic_comment',
        'vid_comment',
        'add_comment',
        'pro_comment',
        'mid_comment',
        'con_comment',
        'pro_comments',
        'add_comments',
        'mid_comments',
        'con_comments'
        ]
    merge_excel = MergeExcel(heads)
    merge_excel.run()
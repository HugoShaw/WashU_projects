# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 23:13:02 2021

@author: Hugo Xue
"""

'''词云图制作'''
from wordcloud import WordCloud
import jieba
import re
import pandas as pd

products = pd.read_excel("products.xlsx")  
df_prod = products.dropna(how="any") 

df_prod["all_comments_content"] = df_prod["name"]+df_prod["pro_comments"]\
+df_prod["add_comments"]+df_prod["mid_comments"]+df_prod["con_comments"]

all_comments_content = df_prod[["all_comments_content"]]
all_comments_content.to_csv('all_comments_content.txt',header=None,index=None,sep=' ',mode='a')

#中文分词
content = open('all_comments_content.txt',encoding='utf-8').read()
content = re.sub("评价"," ",content)
content = re.sub("未填写"," ",content)
content = re.sub("用户"," ",content)
content = re.sub("内容"," ",content)
content = re.sub("京东"," ",content)
content = re.sub("收到"," ",content)

content = re.sub("不错"," ",content)
content = re.sub("买"," ",content)
content = re.sub("不好"," ",content)
content = re.sub("喜欢"," ",content)
content = re.sub("满意"," ",content)
content = re.sub("好用"," ",content)
content = re.sub("没用"," ",content)
content = re.sub("垃圾"," ",content)
content = re.sub("好评"," ",content)
content = re.sub("差评"," ",content)
content = ' '.join(jieba.cut(content))

# 停用词
stpwrd = []
with open('stopwords.txt','r',encoding='utf-8') as f:
    stopwords = f.readlines()
    for words in stopwords:
        stpwrd.append(words.strip('\n'))

#生成词云对象
wc = WordCloud(background_color='white',scale=1.5,stopwords=stpwrd).generate(content)

#显示词云
from matplotlib import pyplot as plt
plt.figure(figsize=(16,9))
plt.imshow(wc)
plt.axis('off')
plt.show()

# 保存到文件
wc.to_file('wordcloud_comments_5.png')
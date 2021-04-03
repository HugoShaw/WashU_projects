# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 22:57:15 2021

@author: Hugo Xue
"""
'''数据预处理'''

import pandas as pd

products = pd.read_excel("products.xlsx")    

products.head() 
products.info()    

# 丢弃行种任意一个没有数据的行
df_prod = products.dropna(how="any")    
df_prod.info()    

df_prod.head().T  
    
## 处理价格
df_prod.loc[:,"price"] = df_prod["price"].apply(lambda x: float(x.strip("￥ ")))    
    
## 处理好评率
df_prod.loc[:,"percent_pro"] = df_prod["percent_pro"].apply(lambda x: float(x.split('\n')[-1].strip("%"))*0.01)
  
## 处理全部评论
df_prod.reset_index(drop=True, inplace=True)
for i in range(len(df_prod)): 
    x = df_prod.loc[i,"all_comment"].split("(")[-1].strip("+)")
    if "万" in x:
        y = float(x.strip("万"))
        z = y*10000
    else:
        z = float(x)      
    df_prod.loc[i,"all_comment"] = float(z)
df_prod["all_comment"] = df_prod["all_comment"].apply(lambda x: float(x))

## 处理晒图评论
df_prod.loc[:,"pic_comment"] = df_prod["pic_comment"].apply(lambda x: float(x.split("(")[-1].strip("+)")))    
    
## 处理视频评论
df_prod.loc[:,"vid_comment"] = df_prod["vid_comment"].apply(lambda x: float(x.split("(")[-1].strip("+)")))    
     
## 处理追评
df_prod.loc[:,"add_comment"] = df_prod["add_comment"].apply(lambda x: float(x.split("(")[-1].strip("+)")))
    
## 处理好评
for i in range(len(df_prod)): 
    x = df_prod.loc[i,"pro_comment"].split("(")[-1].strip("+)")
    if x.find("万") != -1:
        y = float(x.strip("万"))
        z = y*10000
    else:
        z = float(x)      
    df_prod.loc[i,"pro_comment"] = float(z)
        
df_prod["pro_comment"] = df_prod["pro_comment"].apply(lambda x: float(x))

## 处理中评
for i in range(len(df_prod)): 
    x = df_prod.loc[i,"mid_comment"].split("(")[-1].strip("+)")
    if "万" in x:
        y = float(x.strip("万"))
        z = y*10000
    else:
        z = float(x)      
    df_prod.loc[i,"mid_comment"] = float(z)
df_prod["mid_comment"] = df_prod["mid_comment"].apply(lambda x: float(x)) 
# 处理差评   
for i in range(len(df_prod)): 
    x = df_prod.loc[i,"con_comment"].split("(")[-1].strip("+)")
    if "万" in x:
        y = float(x.strip("万"))
        z = y*10000
    else:
        z = float(x)      
    df_prod.loc[i,"con_comment"] = float(z)  
df_prod["con_comment"] = df_prod["con_comment"].apply(lambda x: float(x))  

    
prep_data = df_prod.iloc[:,1:10] 
    
prep_data.info() 

#保存数据
prep_data.to_csv("prep_data.csv",encoding="utf-8")
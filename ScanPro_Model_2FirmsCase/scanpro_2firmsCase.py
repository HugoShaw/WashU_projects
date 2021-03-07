# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 16:35:39 2021

@author: Hugo Xue
"""

''' Scan*Pro model '''

import pandas as pd 
import numpy as np
import statsmodels.formula.api as smf

'''two stores case'''
class ScanPro(object):
    def __init__(self, lnQ, lnP, lnPc, F, D):
        self.data = pd.DataFrame({
            "log_A_Sales": lnQ,
            "log_A_price":lnP,
            "log_B_price":lnPc,
            "A_feature":F,
            "A_display":D
            })
    
    def linear_regression(self):
        regfit = smf.ols(
            'log_A_Sales~log_A_price+log_B_price+A_feature+A_display',
            data=self.data
            ).fit()

        self.results(regfit)
    
    def results(self, regfit):
 
        brand_equity = regfit.params[0]
        
        Own_price_elasticity = regfit.params[1]
        
        Baseline_sales = np.exp(regfit.params[0])
        
        if regfit.pvalues[3] < 0.05:
            Feature_multiplier = np.exp(regfit.params[3])
        else:
            Feature_multiplier = 1
        
        if regfit.pvalues[4] < 0.05: 
            Display_multiplier = np.exp(regfit.params[4])
        else:
            Display_multiplier = 1
        
        Cross_price_elasticity = regfit.params[2]
        
        res = "Brand Equity of store A: {0},\n Own Price Elasticity of store A:{1},\n Baseline Sales of store A: {2},\n Feature Multiplier of store A: {3},\n Display Multiplier of Store A: {4},\n Cross Elasticity of Store A: {5}".format(
            brand_equity,Own_price_elasticity,Baseline_sales,Feature_multiplier,
            Display_multiplier,Cross_price_elasticity)
    
        print(res)
    
    def main(self):
        self.linear_regression()
        

'''storeA'''
col_names = [
    "Maxwell_Sales", "Folgers_Sales", "Week", "StoreA", "StoreB",
    "Maxwell_Price", "Folgers_Price", "Maxwell_Display", "Folgers_Display",
    "Maxwell_Feature", "Folgers_Feature"
    ]

data = pd.read_excel("data.xlsx", header = None, names = col_names)

df = data.iloc[2:,].reset_index(drop=True)

df3 = df[df['StoreA']==1]
df4 = df[df['StoreB']==1]

lnQ = df3['Folgers_Sales'].apply(lambda x: np.log(x))
lnQ2 = df4['Maxwell_Sales'].apply(lambda x: np.log(x))

lnP = df3['Folgers_Price'].apply(lambda x: np.log(x))
lnP2 = df4['Maxwell_Price'].apply(lambda x: np.log(x))

lnPc = df3['Maxwell_Price'].apply(lambda x: np.log(x))
lnPc2 = df4['Folgers_Price'].apply(lambda x: np.log(x))

F = df3['Folgers_Feature'].astype('float64')
F2 = df4['Maxwell_Feature'].astype('float64')

D = df3['Folgers_Display'].astype('float64')
D2 = df4['Maxwell_Display'].astype('float64')

ScanPro(lnQ=lnQ, lnP=lnP, lnPc=lnPc, F=F, D=D).main()
ScanPro(lnQ=lnQ2, lnP=lnP2, lnPc=lnPc2, F=F2, D=D2).main()


# col_names = [
#     "Maxwell_Sales", "Folgers_Sales", "Week", "StoreA", "StoreB",
#     "Maxwell_Price", "Folgers_Price", "Maxwell_Display", "Folgers_Display",
#     "Maxwell_Feature", "Folgers_Feature"
#     ]

# data = pd.read_excel("data.xlsx", header = None, names = col_names)

# df = data.iloc[2:,].reset_index(drop=True)

# df.info()

# df2 = df[df['StoreA'] == 0]

# # target is maxwell 
# lnQ = df2['Maxwell_Sales'].apply(lambda x: np.log(x))

# lnP = df2['Maxwell_Price'].apply(lambda x: np.log(x))

# lnPc = df2['Folgers_Price'].apply(lambda x: np.log(x))

# temp = pd.DataFrame({
#     "log_Maxwell_Sales":lnQ,
#     "log_Maxwell_Price":lnP,
#     "log_Folgers_Price":lnPc,
#     "Maxwell_Feature":df.Maxwell_Feature.astype("float64"),
#     "Maxwell_Display":df.Maxwell_Display.astype("float64")})

# temp.info()

# mod = smf.ols(
#     'log_Maxwell_Sales~log_Maxwell_Price+log_Folgers_Price+Maxwell_Feature+Maxwell_Display',
#     data = temp)

# res = mod.fit()

# print(res.summary())
# print(res.params)
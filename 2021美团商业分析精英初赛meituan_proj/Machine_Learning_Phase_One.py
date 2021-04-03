# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 23:00:02 2021

@author: Hugo Xue
"""

'''针对销售额数据(无情感分析得分)，进行预测'''
import pandas as pd
from sklearn.model_selection import train_test_split

prep_data = pd.read_csv("prep_data.csv")

predictors = prep_data.columns.difference(["all_comment"])

X_train, X_test, y_train, y_test = train_test_split(
    prep_data[predictors], 
    prep_data[["all_comment"]],
    random_state=666,
    test_size = 0.3
    )

from sklearn.preprocessing import StandardScaler
ss_X = StandardScaler()
ss_y = StandardScaler()

X_train = ss_X.fit_transform(X_train)
X_test = ss_X.transform(X_test)
y_train = ss_y.fit_transform(y_train)
y_test = ss_y.transform(y_test)

# 线性回归模型
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(X_train,y_train)
# 预测数据
lr_y_predict = lr.predict(X_test)
# 模型精度 0.667
lr.score(X_test,y_test)
# mse 12367981981.29658
from sklearn.metrics import mean_squared_error
mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(lr_y_predict))
lr.coef_

# SGDregressor 0.7291609473143316
from sklearn.linear_model import SGDRegressor
sgdr = SGDRegressor()
sgdr.fit(X_train,y_train.ravel())
sgdr_y_predict = sgdr.predict(X_test)
sgdr.score(X_test,y_test)
sgdr.coef_

# KNN  0.8601679311980618
from sklearn.neighbors import KNeighborsRegressor
dis_knr = KNeighborsRegressor(weights="distance")
dis_knr.fit(X_train,y_train)
dis_knr_y_predict = dis_knr.predict(X_test)
dis_knr.score(X_test,y_test)

# Tree -0.061326986019740515
from sklearn.tree import DecisionTreeRegressor
dtr = DecisionTreeRegressor()
dtr.fit(X_train,y_train)
dtr_y_predict = dtr.predict(X_test)
dtr.score(ss_y.inverse_transform(X_test),ss_y.inverse_transform(y_test))

# random forest, boosting 
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor, GradientBoostingRegressor
bag = BaggingRegressor()
bag.fit(X_train, y_train.ravel())
bag_y_predict = bag.predict(X_test)
bag.score(ss_y.inverse_transform(X_test),ss_y.inverse_transform(y_test))

rf = RandomForestRegressor()
rf.fit(X_train, y_train.ravel())
rf_y_predict = rf.predict(X_test)
rf.score(ss_y.inverse_transform(X_test),ss_y.inverse_transform(y_test))

boost = GradientBoostingRegressor()
boost.fit(X_train, y_train.ravel())
boost_y_predict = boost.predict(X_test)
boost.score(ss_y.inverse_transform(X_test),ss_y.inverse_transform(y_test))
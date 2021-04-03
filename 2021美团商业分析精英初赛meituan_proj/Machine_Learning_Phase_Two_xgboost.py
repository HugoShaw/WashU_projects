# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 23:17:21 2021

@author: Hugo Xue

"""

'''加入情感得分后进行机器学习预测分析'''

import pandas as pd 

prep_data = pd.read_csv("prep_data.csv")    
comments_sentiment = pd.read_excel('jd_sentiment_scores.xlsx')

prep_data["sentiment_scores"] = comments_sentiment["sentiment"]
prep_data.info()

from sklearn.model_selection import train_test_split
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

# 0.743
from sklearn.linear_model import SGDRegressor
sgdr = SGDRegressor()
sgdr.fit(X_train,y_train.ravel())
sgdr_y_predict = sgdr.predict(X_test)
sgdr.score(X_test,y_test)
sgdr.coef_

# 0.859
from sklearn.neighbors import KNeighborsRegressor
dis_knr = KNeighborsRegressor(weights="distance")
dis_knr.fit(X_train,y_train)
dis_knr_y_predict = dis_knr.predict(X_test)
dis_knr.score(X_test,y_test)

from sklearn.tree import DecisionTreeRegressor
dtr = DecisionTreeRegressor()
dtr.fit(X_train,y_train)
dtr_y_predict = dtr.predict(X_test)
dtr.score(ss_y.inverse_transform(X_test),ss_y.inverse_transform(y_test))

from matplotlib import pyplot as plt 

plt.scatter(prep_data["sentiment_scores"],prep_data["all_comment"])

plt.scatter(prep_data["price"],prep_data["all_comment"])
plt.show()

'''log transform 这个好像不大行'''
prep_data.info()

import numpy as np
import statsmodels.formula.api as smf
prep_data['log_price'] = np.log(prep_data["price"])
prep_data["sales"] = np.log(prep_data["all_comment"])

predictors = "+".join(prep_data.columns.difference(["price","all_comment","sales"]))

ssx = StandardScaler()
ssy = StandardScaler()

X = prep_data
x = ssx.fit_transform(prep_data.loc[:,"price":"log_price"])
y = ssy.fit_transform(prep_data.loc[:,"sales"])
X.loc[:,"price":"log_price"] = x
X.loc[:,"sales"] = y

# sentiment_scores are highly related, -0.8084, negative relationship 
result = smf.ols("sales~{}".format(predictors),data=X).fit()
print(result.summary())


'''xgboost-bayesian optimization'''
from xgboost import XGBRegressor
import xgboost as xgb
from bayes_opt import BayesianOptimization
from sklearn.model_selection import train_test_split
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

# accuracy 
clf_xgb1 = XGBRegressor().fit(X_train,y_train)
train_p1 = clf_xgb1.predict(X_train)
test_p1 = clf_xgb1.predict(X_test)
print(clf_xgb1.score(X_test,y_test))

dtrain = xgb.DMatrix(X_train,y_train)

def tune_xgb(min_child_weight,max_depth,n_estimators,col_sample_bytree,gamma,alpha):
    params = {
        "learning_rate":0.1,
        "subsample":0.8,
        "seed":27,
        "eta":0.1,
        "eval_metric":"rmse",
        "min_child_weight":min_child_weight,
        "max_depth":int(max_depth),
        "num_parallel_tree":int(n_estimators),
        "colsample_bytree":col_sample_bytree,
        "gamma":gamma,
        "alpha":alpha
        }
    
    # num_boost_round值增大，运算次数增多，精度可能更高，但是会很慢
    xgb_cv = xgb.cv(params, dtrain, num_boost_round=50,nfold=3)
    
    # 最大化-MAE，即最小化MAE（平均误差绝对值）
    return -1*xgb_cv['test-rmse-mean'].iloc[-1]

xgb_bo = BayesianOptimization(tune_xgb,{
    "min_child_weight":(1,20),
    "max_depth":(5,15),
    "n_estimators":(10,100),
    "col_sample_bytree":(0.1,1),
    "gamma":(0,1),
    "alpha":(0,1)
    })

xgb_bo.maximize()
# 所有迭代后生成的参数
xgb_bo.space.params
# 所有迭代后生成的参数
xgb_bo.res
# 最佳参数
best_params = xgb_bo.max['params']
print(best_params)

#Conversting the max_depth and n_estimator values from float to int
best_params['max_depth']= int(best_params['max_depth'])
best_params['n_estimators']= int(best_params['n_estimators'])
print(best_params['max_depth'])
print(best_params['n_estimators'])

# 手动修改下参数名称
best_params = {
    "learning_rate":0.1,
    "subsample":0.8,
    "seed":27,
    "eta":0.1,
    "eval_metric":"rmse",
    'alpha': 0.619322126829407, 
    'colsample_bytree': 0.9470877980403922, 
    'gamma': 0.2556717840686624, 
    'max_depth': 6, 
    'min_child_weight': 1.269749212001932, 
    'n_estimators': 35}

# using the tuned params to fit the test data 30.98%
clf_xgb = XGBRegressor(**best_params).fit(X_train,y_train)
y_pred = clf_xgb.predict(X_train)
# 对训练集的精度达到 0.8174
print(clf_xgb.score(X_test,y_test))


# 画下实际和预测的数据线型图，看看xgboost拟合情况
fig = plt.figure(figsize=(40,20))
plt.plot(y_pred)
plt.plot(y_train)
plt.legend(["predicted sales","real sales"])
plt.show()




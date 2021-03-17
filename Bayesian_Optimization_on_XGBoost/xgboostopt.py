# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 12:21:54 2021

@author: Hugo Xue
"""

import pandas as pd 
# import numpy as np

'''导入数据'''
data = pd.read_excel("aaa.xlsx")

print(data.info())

# 删除空值列
# dt = data.drop(columns=['log（资产）','资产总计（亿元）'])

# 对空值的行进行填充，填充值为0
dt = data.fillna(0)

# 对数据类型进行转换
# row 488 data is problematic
dt.iloc[488,23] = 74.6357
dt.iloc[:,23] = dt.iloc[:,23].map(lambda x: float(x))

# 数据共有1790行
# 样本总数不多，3/7分数据集进行训练评估
dt.info()

'''导入数据'''
# from sklearn.preprocessing import MinMaxScaler

# 查看数据结构/维度
dt.shape

# 对数据进行分割
y = dt["主体评级\r\n[交易日期] 2019-12-31\r\n[评级机构] 国内评级机构(除中债资信)\r\n[评级对象类型] 主体信用评级"].values
x = dt[['中央国企', '地方国企', '民营企业', '房地产行业', '采矿业', '电力、热力、燃气及水生产和供应业', '建筑业',
       '交通运输、仓储和邮政业', '金融业', '科学研究和技术服务业', '农、林、牧、渔业', '批发和零售业',
       '水利、环境和公共设施管理业', '文化、体育和娱乐业', '信息传输、软件和信息技术服务业', '制造业', '住宿和餐饮业', '综合',
       '租赁和商务服务业', 'log（资产）', '资产负债率\n[报告期]去年年报\n[单位] %', '权益乘数\r\n[报告期] 去年年报',
       '产权比率\r\n[报告期] 去年年报', '流动比率\r\n[报告期] 去年年报', '现金比率\r\n[报告期] 去年年报',
       'ROA\n[报告期] 去年年报\n[单位] %', 'ROE(平均)\n[报告期] 去年年报\n[单位] %',
       '存货周转率\r\n[报告期] 去年年报\r\n[单位] 次', '应收账款周转率',
       '流动资产周转率\r\n[报告期] 去年年报\r\n[单位] 次', '利息保障倍数\n[报告期] 去年年报',
       '销售净利率\r\n[报告期] 去年年报\r\n[单位] %', '销售毛利率\r\n[报告期] 去年年报\r\n[单位] %',
       '营业利润率\n[报告期] 去年年报\n[单位] %',
       '研发支出总额占营业收入比例\r\n[报告期] 去年年报\r\n[报表类型] 合并报表\r\n[单位] %',
       '现金流量比率\n[报告期] 去年年报']].values

cols = ['中央国企', '地方国企', '民营企业', '房地产行业', '采矿业', '电力、热力、燃气及水生产和供应业', '建筑业',
       '交通运输、仓储和邮政业', '金融业', '科学研究和技术服务业', '农、林、牧、渔业', '批发和零售业',
       '水利、环境和公共设施管理业', '文化、体育和娱乐业', '信息传输、软件和信息技术服务业', '制造业', '住宿和餐饮业', '综合',
       '租赁和商务服务业', 'log（资产）', '资产负债率\n[报告期]去年年报\n[单位] %', '权益乘数\r\n[报告期] 去年年报',
       '产权比率\r\n[报告期] 去年年报', '流动比率\r\n[报告期] 去年年报', '现金比率\r\n[报告期] 去年年报',
       'ROA\n[报告期] 去年年报\n[单位] %', 'ROE(平均)\n[报告期] 去年年报\n[单位] %',
       '存货周转率\r\n[报告期] 去年年报\r\n[单位] 次', '应收账款周转率',
       '流动资产周转率\r\n[报告期] 去年年报\r\n[单位] 次', '利息保障倍数\n[报告期] 去年年报',
       '销售净利率\r\n[报告期] 去年年报\r\n[单位] %', '销售毛利率\r\n[报告期] 去年年报\r\n[单位] %',
       '营业利润率\n[报告期] 去年年报\n[单位] %',
       '研发支出总额占营业收入比例\r\n[报告期] 去年年报\r\n[报表类型] 合并报表\r\n[单位] %',
       '现金流量比率\n[报告期] 去年年报']
# 数据归一化
# min_max_scaler = MinMaxScaler(feature_range=(0,1))
# X = min_max_scaler.fit_transform(x)

X_train = x[:int(len(x)*0.7),:]
X_test = x[int(len(x)*0.7):,:]
y_train = y[:int(len(y)*0.7)]
y_test = y[int(len(y)*0.7):]

'''使用sklearn已有的分类器,并设置参数'''
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
import xgboost as xgb
from bayes_opt import BayesianOptimization

clf_xgb1 = XGBClassifier().fit(X_train,y_train)
train_p1 = clf_xgb1.predict(X_train)
test_p1 = clf_xgb1.predict(X_test)
print(classification_report(train_p1,y_train))
print(classification_report(test_p1,y_test))
cm = confusion_matrix(y_train,train_p1)
accuracy = cm.diagonal().sum()/cm.sum()
print(accuracy)

# params = {
#     "learning_rate":0.1,
#     "subsample":0.8,
#     "seed":27,
#     "eta":0.1,
#     "eval_metric":"mae",
#     "min_child_weight":1,
#     "max_depth":5,
#     "n_estimators":10,
#     "colsample_bytree":0.1,
#     "gamma":0,
#     "reg_alpha":0
#     }

# xgb_cv2 = xgb.cv(params, dtrain, num_boost_round=11, nfold=3)
# xgb_cv2

dtrain = xgb.DMatrix(X_train,y_train)

def tune_xgb(min_child_weight,max_depth,n_estimators,col_sample_bytree,gamma,alpha):
    params = {
        "learning_rate":0.1,
        "subsample":0.8,
        "seed":27,
        "eta":0.1,
        "eval_metric":"mae",
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
    return -1*xgb_cv['test-mae-mean'].iloc[-1]

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
    "eval_metric":"mae",
    'alpha': 0.00845119738463751, 
    'colsample_bytree': 0.9577000525280355, 
    'gamma': 0.9866950561841166, 
    'max_depth': 9, 
    'min_child_weight': 1.6797841956957478, 
    'n_estimators': 11}

# using the tuned params to fit the test data
clf_xgb = XGBClassifier(**best_params).fit(X_train,y_train)
y_pred = clf_xgb.predict(X_train)
# 对训练集的精度达到0.89
print(classification_report(y_train,y_pred))

# 对测试集的精确度只有32%
y_pred_val = clf_xgb.predict(X_test)
print(classification_report(y_test,y_pred_val))

# confusion matrix
tuned_cm = confusion_matrix(y_train, y_pred)
tuned_acc = tuned_cm.diagonal().sum()/tuned_cm.sum()
print(tuned_acc)


















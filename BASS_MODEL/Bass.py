# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 20:12:51 2021

@author: Hugo Xue
@email: hugo@wustl.edu
"""
import numpy as np
import pandas as pd

'''construct a BASS MODEL'''
class BASS(object):
    def __init__(self, p, q, m, period=10):
        print("Hi! Hugo wants you know several things below:")
        print("==============================================")
        print("input your p,q,m,and periods(months/quarters/years)")
        print("continuous/discrete/repeated bass model is optional")
        print("BASS has 3 functions: .continuous/.discrete/.repeat")
        print("It will return a dataframe as your result")
        print("==============================================")
        # self.p = float(input("pls input p: "))
        # self.q = float(input("pls input q: "))
        # self.m = float(input("pls input m: "))
        # self.period = int(input("pls input time (how many quarters): "))
        self.p = p
        self.q = q
        self.m = m
        self.period = period
        
        
    def continuous(self):
        Nt = []
        At1 = []
        
        p = self.p
        q = self.q
        m = self.m
        t = self.period
        periods = np.linspace(1,t,t,dtype=int)
        
        # Continuous Bass Model
        for i in range(1,int(t)+1,1):
            A_t1 = m * (1-np.exp(-(p+q)*(i-1)))/(1+(q/p)*(np.exp(-(p+q)*(i-1))))
            A_t = m * (1-np.exp(-(p+q)*i))/(1+(q/p)*(np.exp(-(p+q)*i)))
            N_t = A_t - A_t1
            At1.append(A_t1)
            Nt.append(N_t)
            
        cbass = pd.DataFrame({"Time":periods,"N(t)":Nt,"A(t-1)":At1})
        
        return cbass
    
    def discrete(self):
        p = self.p
        q = self.q
        m = self.m
        t = self.period
        periods = np.linspace(1,t,t,dtype=int)

        N_predict = [0]
        A_predict = [0]
        
        for i in range(1,len(periods)+1):
            Rt = m - A_predict[i-1]
            A0 = 0
            Ht = p + q * (A_predict[i-1]/m)
            Nt = Ht * Rt
            N_predict.append(Nt)
            for n in range(len(N_predict)):
                A0 += N_predict[n]
            A_predict.append(A0)
        
        N_predict.pop(0)
        A_predict.pop(0)
        
        dbass = pd.DataFrame({"Time":periods,"N(t)":N_predict,"A(t)":A_predict})
        
        return dbass
    
    def repeat(self):
        p = self.p
        q = self.q
        m = self.m
        t = self.period
        rep = int(input("pls input the frequency of the repeat purchase: "))
        periods = np.linspace(1,t,t,dtype=int)
    
        N_predict = [0]
        A_predict = [0]
        
        for i in range(1,len(periods)+1):
            Rt = m - A_predict[i-1]
            A0 = 0
            Ht = p + q * (A_predict[i-1]/m)
            Nt = Ht * Rt
            N_predict.append(Nt)
            for n in range(len(N_predict)):
                A0 += N_predict[n]
            A_predict.append(A0)
        
        N_predict.pop(0)
        A_predict.pop(0)
        
        Sales_pred = []
        
        for i in range(1,len(N_predict)+1,1):
            s_count = 0
            if i < rep+1:
                Sales_pred.append(N_predict[i-1])
            else:
                seq_len = (int(i/rep) - 1)*rep+(i%rep)
                seq_count = 0
                for j in range(seq_len):
                    seq_count += N_predict[j]
                s_count = N_predict[i-1] + seq_count
                Sales_pred.append(s_count)
                
        rbass = pd.DataFrame({
            "Time":periods,"N(t)":N_predict,"A(t)":A_predict,"Sales":Sales_pred})
        
        return rbass


# test the accuracy
# if __name__ == '__main__':
#     result = BASS(p=0.0058480419267518124,q=0.05749225793093697,m=23308450.26524349,period=48)
#     result.continuous()
    
    

        
        
    

































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
        
        for i in range(1,len(periods)):
            Rt = m - A_predict[i-1]
            A0 = 0
            Ht = p + q * (A_predict[i-1]/m)
            Nt = Ht * Rt
            N_predict.append(Nt)
            for n in range(len(N_predict)):
                A0 += N_predict[n]
            A_predict.append(A0)
        
        dbass = pd.DataFrame({"Time":periods,"N(t-1)":N_predict,"A(t-1)":A_predict})
        
        return dbass
    
    def repeat(self):
        p = self.p
        q = self.q
        m = self.m
        t = self.period
        rep = int(input("pls input the frequency of the repeat purchase: "))
        periods = np.linspace(1,t,t,dtype=int)
    
        Nt = []
        At = []
        
        # Continuous Bass Model
        for i in range(1,int(t)+1,1):
            A_t1 = m * (1-np.exp(-(p+q)*(i-1)))/(1+(q/p)*(np.exp(-(p+q)*(i-1))))
            A_t = m * (1-np.exp(-(p+q)*i))/(1+(q/p)*(np.exp(-(p+q)*i)))
            N_t = A_t - A_t1
            At.append(A_t)
            Nt.append(N_t)
        
        Sales_pred = []
        
        for row in range(1,len(Nt)+1,1):
            if row < rep+1:
                Sales_pred.append(Nt[row-1])
            else:
                s_count = 0
                rd = int(row/rep)
                for r in range(rd): 
                    idx = (int(row/rep) - 1)*rep+(row%rep)
                    s_count += Nt[row-1]
                    s_count += Nt[idx-1]
                    row -= rep
                
                Sales_pred.append(s_count)
                
        rbass = pd.DataFrame({
            "Time":periods,"N(t)":Nt,"A(t)":At,"Sales":Sales_pred})
        
        return rbass


# test the accuracy
# if __name__ == '__main__':
#     result = BASS(p=0.00645,q=0.058974,m=22433724,period=400)
#     result.continuous()
#     result.discrete()
#     result.repeat()
    
    

        
        
    

































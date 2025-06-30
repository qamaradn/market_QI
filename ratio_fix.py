# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 10:55:00 2023

@author: qamara
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import RobustScaler
from sklearn.utils import resample

def data_ratio(path,filename,filename_ratio,n):
    df_comb=pd.read_csv(path+filename, header=0)
    #scaler = MinMaxScaler()
    #scaler = StandardScaler()
    #scaler = MaxAbsScaler()
    #robust = RobustScaler(quantile_range = (0.1,0.9))
    #df_comb[df_comb.columns[1:6]] = scaler.fit_transform(df_comb[df_comb.columns[1:6]])    #0.9   #-0.02
    mask = df_comb[df_comb.columns[-1]] > 20 #20 
    comb = df_comb.drop(df_comb[mask].index)
    
    mask1 = comb[comb.columns[-1]] < -0.02 
    comb = comb.drop(comb[mask1].index)
    
    comb = comb.sort_values(comb.columns[-1],ascending=False)
    comb.reset_index(drop=True, inplace=True)
    
    s11=(comb['label5'] == 1).sum()
    minority_class = comb[comb['label5'] == 1]
    
    #comb.drop(comb.tail(n=50000).index,inplace=True)
    # Oversample the minority class
    oversampled_minority = resample(minority_class, replace=True, n_samples=s11, random_state=42)

    # oversampling 0 class ##############
    s10=(comb['label5'] == 0).sum()
    minority_class0 = comb[comb['label5'] == 0]
    oversampled_minority0 = resample(minority_class0, replace=True, n_samples=s10, random_state=42)
    for _ in range(3):
     comb = pd.concat([comb, oversampled_minority0])
    ################## 
    
    # Add the oversampled minority back to the original DataFrame
    s0 =(comb['label5'] == 0).sum()
    s1=(comb['label5'] == 1).sum()
    pos=s0/s1
    #n=4
    #n=int(pos)
    for _ in range(n-1):
     comb = pd.concat([comb, oversampled_minority])
    
    #comb.drop(comb.tail(n=500).index,inplace=True)
    
    s0 =(comb['label5'] == 0).sum()
    s1=(comb['label5'] == 1).sum()
    pos=s1/s0
    
    #print(comb.tail(n=50))
    #comb.drop(comb.tail(n=5000).index,inplace=True)
     
    comb.to_csv(path+filename_ratio,index=False,header=True,mode ='w')
    return None
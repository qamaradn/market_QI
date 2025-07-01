# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 19:27:00 2022

@author: qamara
"""

import numpy as np
import pandas as pd

def data_clean(path,file_name):
    skipday=2
    df1 = pd.read_csv(path+file_name, header=[0,1,2],low_memory=False)
    df1=df1.iloc[::skipday]
    df1=pd.concat([df1,pd.concat([df1[-1:]])])  # duplicate last row 
    # df2 = pd.read_csv('NSE2.csv', header=None,low_memory=False)
    # df3 = pd.read_csv('NSE3.csv', header=None,low_memory=False)
    # df4 = pd.read_csv('NSE4.csv', header=None,low_memory=False)
    
    df1.columns = df1.columns.droplevel([1,2])
    
    #df1 = df1.drop(labels=[1,2], axis=0)
    df1 = df1.drop(columns=df1.columns[0])
    df1.reset_index(drop=True, inplace=True)
    
    #header=df1.loc[0,:]
    #df1.columns=header
    #df1 = df1.drop(labels=0, axis=0)
    df1.reset_index(drop=True, inplace=True)
    #df1.dropna(axis=1,thresh=200, how="any")
    df1=df1.dropna(axis=1, how="all") # replace column by all Nan values
    df1=df1.dropna(axis=0, how="all") # replace row by all Nan values
    df1 = df1.astype(float)
    df1 = df1.interpolate(method='linear', axis=0).ffill().bfill() # replace Nan by interpolation 
    #df =df1.apply(lambda x: x.fillna(x.mean()),axis=0) # replace Nan by average of each column
    # m=df1.mean(numeric_only=True,axis=0)
    print(df1)
    data =df1
           
    close=data.iloc[:,::5].T
    high=data.iloc[:,1::5].T
    low=data.iloc[:,2::5].T
    open1=data.iloc[:,3::5].T
    volume=data.iloc[:,4::5].T
    
    #-------------------------------------------------------
    col_2nd_last = close.iloc[:,-2]
    col_3rd_last = close.iloc[:,-3]

    # Calculate the difference between the 2nd last and 3rd last row
    difference = col_2nd_last - col_3rd_last

    # Count positive and negative differences
    positive_count = len(difference[difference > 0])
    negative_count = len(difference[difference < 0])

    print("Number of positive differences:", positive_count)
    print("Number of negative differences:", negative_count)
    print("Ratio:",positive_count/negative_count)
# ------------------------------------------------------
    
    open1.to_csv(path+'open.csv',index=True,header=False,mode ='w')
    high.to_csv(path+'high.csv',index=True,header=False,mode ='w')
    low.to_csv(path+'low.csv',index=True,header=False,mode ='w')
    close.to_csv(path+'close.csv',index=True,header=False,mode ='w')
    volume.to_csv(path+'volume.csv',index=True,header=False,mode ='w')
    return close.shape[0], close.shape[1]
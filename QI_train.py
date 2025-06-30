# -*- coding: utf-8 -*-
"""
Created on Sat 5ec  5 14:56:42 2020
@author: Adnan Qamar, Water Desalination and Reuse Center, KAUST.
Email : Adnan.Qamar@kaust.edu.sa
"""

#def backtest(back_test):

import numpy as np
from qamar_single import QI
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def data_QI(start_day,end_day,path_qi,file_input,trainfile_output,N,start,testfile_output):
    file_list=['close.csv','high.csv','open.csv','low.csv','volume.csv']
    #avg=[]
    df_comb = pd.DataFrame()
    

    df_label = pd.DataFrame()
    df_infer=pd.read_csv(path_qi+file_input, header=None)
    for k in range(start_day,end_day):  #(0,1) for last day from data for infer
        
    #df_combine = pd.DataFrame()
        df_tick = pd.read_csv(path_qi+'close.csv', header=None) 
        df_combine=pd.DataFrame(df_tick[df_tick.columns[0]])
        
        #file_list=['close.csv','high.csv']
        for i in file_list:
            df = pd.read_csv(path_qi+i, header=None) 
            #print(k,N,df.shape[1])
            #back_test=df.shape[1]-k-1
            
            back_test=df.shape[1]-N+k-1    #last two day data not able to compute flag , this subtract another two days so total if 2 value it means last 4th day 
            ###print (back_test,df.shape[1],N,k)
        #df.drop(df.iloc[:, -back_test:], axis=1, inplace=True)
            df,df_asc= QI(path_qi,back_test,df,i)
            #print(k,N,back_test,df.shape[1])
            df_combine = df_combine.join(df_asc[i])
            df_combine[i] = pd.to_numeric(df_combine[i])
           
        ###print(df.head())   
        #df_label = pd.DataFrame()
        df_labe = []
        for j in range(N-k,df_infer.shape[0],N-1+start-1):
            df_labe.append(df_infer.iloc[j,6:8])
             
        df_label = pd.DataFrame(df_labe)
        
        
        df_label.columns=['label1','label5']
        df_label.reset_index(drop=True, inplace=True)
        #df_label['label1'] = pd.to_numeric(df_label['label1'])    
        df_combine = df_combine.join(df_label['label5'])
        df_combine = df_combine.join(df_label['label1'])
        
        df_comb=pd.concat([df_comb,df_combine])
    
    #open these commented files for live market predictions
    df_comb.iloc[:df.shape[0]].to_csv(path_qi+testfile_output,index=False,header=True,mode ='w')
    #df_comb.iloc[df.shape[0]:df.shape[0]*2].to_csv(path_qi+testfile_output,index=False,header=True,mode ='w')
    #df_comb.iloc[df.shape[0]*2:].to_csv(path_qi+trainfile_output,index=False,header=True,mode ='w')
    df_comb.iloc[df.shape[0]:].to_csv(path_qi+trainfile_output,index=False,header=True,mode ='w')
    return None
   
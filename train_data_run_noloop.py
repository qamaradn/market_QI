# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 19:27:00 2022

@author: qamara
"""

import numpy as np
import pandas as pd
from RSI_index import train_data
from data_fix import data_clean
from ratio_fix import data_ratio
from QI_train import data_QI
#from stock_qamarQI_xgboost_reg import QIML
from stock_qamarQI_xgboost_reg import QIML
import matplotlib.pyplot as plt



path='C:/Users/Adnan Qamar/Desktop/AWS/code_aws/code_aws/'
file_name='data_test.csv'
#file_name='NSE1.csv'
filename_out = 'training_aug_oct.csv'
filename_ratio='training_ratio.csv'
trainfile_output = 'trainQI.csv'
testfile_output='testQI.csv'
per_diff=1
start_day=1 #greater than window size
end_day=10  # should be > 1 : how many day you wanna go backward from last coumn of N
nn= 1 # number of oversampling times 
gain=[]
kk=2#40  # (kk-1) is the number skipps from last days. kk=3, mean (kk-1=2) last two colums of data files are left for prediction
#for kk in range(10,45,5):
start=kk
start1=1
end_day1=(start-start1)+1

##########
#g_l=0.0
#sv=0.0
#sc=0.0
#i_nv=0.0
#i_nc=0.0
#profit=0.0
li=[]
out=[]
df11 = pd.read_csv(path+file_name, header=None,low_memory=False)
for k in range(1,2):
    
    # genrate close, open , high, low, volume files from NSE1.csv
    i,j=data_clean(path,file_name)  
    print(i,j)
    N=j-start+2   #total number of data to be included from 0-df.shape[1]
    N1=j-start1 

    # genrate filename_out file with data stacked for all stock
    train_data(path,per_diff,filename_out)

    #generate QItraining and file 
    data_QI(start_day,end_day,path,filename_out,trainfile_output,N,start,testfile_output)  # 40 mean leave last 40 days data dor prediction
    #data_QI(start_day,end_day1,path,filename_out,testfile_output,N1,start1)  

    #genrate oversampled data for under-represented class 
    data_ratio(path,trainfile_output,filename_ratio,nn)

    #ML Training and Prediction 
    print(i,j,kk)
    
    comp1,li,per=QIML(path,i,testfile_output,'label5','Xgboost',0,1)
    print('Iteration:',li,1)
    #comp1 = comp1.rename(columns={'0': 'Comp'})
    #print(comp1)
    comp2,li,per=QIML(path,li,testfile_output,'label5','Xgboost',0,2)
    print('Iteration:',li,2)
    comp3,li,per=QIML(path,li,testfile_output,'label5','Xgboost',0,3)
    print('Iteration:',li,3)
    comp4,li,per=QIML(path,li,testfile_output,'label5','Xgboost',0,4)
    print('Iteration:',li,4)
    
    comp5,li,per=QIML(path,li,testfile_output,'label5','Xgboost',0,5)
    print('Iteration:',li,5)
    comp6,li,per=QIML(path,li,testfile_output,'label5','Xgboost',0,6)
    print('Iteration:',li,6)
    comp7,li,per=QIML(path,li,testfile_output,'label5','Xgboost',0,7)
    print('Iteration:',li,7)
    comp8,li,per=QIML(path,li,testfile_output,'label5','Xgboost',0,8)
    print('Iteration:',li,8)
    
    comp9,li,per=QIML(path,li,testfile_output,'label5','Xgboost',0,9)
    print('Iteration:',li,9)
    comp10,li,per=QIML(path,li,testfile_output,'label5','Xgboost',0,10)
    print('Iteration:',li,10)
    comp11,li,per=QIML(path,li,testfile_output,'label5','Xgboost',0,11)
    print('Iteration:',li,11)
    comp12,li,per=QIML(path,li,testfile_output,'label5','Xgboost',0,12)
    print('Iteration:',li,12)


    merged_df = pd.concat([comp1,comp2,comp3,comp4,comp5,comp6,comp7,comp8,comp9,comp10,comp11,comp12])
    result = merged_df.groupby(merged_df.columns[0])['Pre_label'].sum().reset_index()
    result_sorted = result.sort_values(by='Pre_label',ascending=True)
    print(result_sorted)
    
    
   
    #li=QIML(path,i,testfile_output,'label5','Extra Trees')
    #print(li)
    # while li > 40:
    #      #li,per=QIML(path,i,testfile_output,'label1','Xgboost',1)
    #      #print(li)
    #      li,per=QIML(path,li,testfile_output,'label5','Xgboost',0)
    #      print(li)
         
         

        
    #      li=QIML(path,li,testfile_output,'label5','Extra Trees')
    #      print(li)
    #      #li=QIML(path,li,testfile_output,'label1','Extra Trees')
    #      #print(li)
    #      li=QIML(path,li,testfile_output,'label5','Neural Network')
    #      print(li)

    
    #[g_l,sv,sc,i_nv,i_nc,profit]=QIML(path,i)
    out.append(per)
    print(out)
    #gain.append(g_l)
    #print(gain)
    df11=df11.iloc[:-1]
    #print(df11)
    df11.to_csv(path+file_name,header=None, index=False,mode='w')
print(sum(out))    
#dfObj = pd.DataFrame(out,columns=['Accuracy','VVolume','VClose','i_nV','i_nC','Profit/loss'])
#print(dfObj)
#print(dfObj['Profit/loss'].sum())
#dfObj.to_csv(path+'analysis.csv',header=True, index=False,mode='w')
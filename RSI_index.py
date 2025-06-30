# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 14:30:15 2021

@author: Adnan Qamar, Water Desalination and Reuse Center, KAUST.
Email : Adnan.Qamar@kaust.edu.sa
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def train_data(path,per_diff,filename_out):
    #per_diff=1 # period for difference for label flags
    
    dfc = pd.read_csv(path+'close.csv', header=None)
    dfc_T =dfc.T
    header=dfc_T.loc[0,:]
    header2=[]   # strip the company name before .NS
    for i in range(len(header)):
        kk=header[i].partition(".")[0]
        header2.append(kk[:])
    
    dfc_T.columns=header2
    dfc_T=dfc_T.drop(labels=0,axis=0)
    dfc_T.reset_index(drop=True, inplace=True)
    
    # genrating labels
    labels=-(dfc_T.diff(axis = 0, periods = -per_diff)/dfc_T)*100  # last two rows should ne NAN or zero 
    #labels=dfc_T.diff(axis = 0, periods = 2)
    #labels=100*dfc_T.pct_change(periods=2)  # % = (current_cell-previous_cell)/previous_cell
    labels = labels.fillna(0)
    df_sig= np.where(labels > 2., 1.,0.) # for 2% profit
    #df_label = pd.DataFrame (df_sig)
    df_label = pd.DataFrame(labels)
    df_label.columns=header2
    
    df_sig= np.where(labels >1, 1.,0.) #for 5% profit
    df_label5 = pd.DataFrame (df_sig)
    #df_label5 = pd.DataFrame (labels)
    df_label5.columns=header2
    #df_label5=(df_label5-df_label5.min())/(df_label5.max()-df_label5.min())
    
    ###df_label5.drop(df_label5.tail(per_diff).index, axis=0, inplace=True) 
    ###df_label.drop(df_label.tail(per_diff).index, axis=0, inplace=True)  
    ###dfc_T.drop(dfc_T.tail(per_diff).index, axis=0, inplace=True) 
    #df_label5.drop(index=df_label5.index[-2], axis=0, inplace=True)
    #df_label=df_label.drop(labels=0,axis=0)
    
    dfo = pd.read_csv(path+'open.csv', header=None)
    dfo_T =dfo.T
    #header=dfo_T.loc[0,:]
    dfo_T.columns=header2
    dfo_T=dfo_T.drop(labels=0,axis=0)
    dfo_T.reset_index(drop=True, inplace=True)
    ###dfo_T.drop(dfo_T.tail(per_diff).index, axis=0, inplace=True) 
    
    dfh = pd.read_csv(path+'high.csv', header=None)
    dfh_T =dfh.T
    #header=dfh_T.loc[0,:]
    dfh_T.columns=header2
    dfh_T=dfh_T.drop(labels=0,axis=0)
    dfh_T.reset_index(drop=True, inplace=True)
    ###dfh_T.drop(dfh_T.tail(per_diff).index, axis=0, inplace=True) 
    
    dfl = pd.read_csv(path+'low.csv', header=None)
    dfl_T =dfl.T
    #header=dfl_T.loc[0,:]
    dfl_T.columns=header2
    dfl_T=dfl_T.drop(labels=0,axis=0)
    dfl_T.reset_index(drop=True, inplace=True)
    ###dfl_T.drop(dfl_T.tail(per_diff).index, axis=0, inplace=True) 
    
    dfv = pd.read_csv(path+'volume.csv', header=None)
    dfv_T =dfv.T
    #header=dfv_T.loc[0,:]
    dfv_T.columns=header2
    dfv_T=dfv_T.drop(labels=0,axis=0)
    dfv_T.reset_index(drop=True, inplace=True)
    ###dfv_T.drop(dfv_T.tail(per_diff).index, axis=0, inplace=True) 
    
    
    
    df_tik1 = pd.DataFrame(header2)
    df_tik1 = df_tik1.T
    df_tik1 = pd.DataFrame(np.repeat(df_tik1.values,dfc_T.shape[0], axis=0))
    
    
    df_combine = pd.DataFrame()
    
    df_infer = pd.DataFrame()
    
    scaler = MinMaxScaler()
    for i in range(dfc_T.shape[1]): 
    #for i in range(1):    
    #df_merge_col = pd.merge(dfc_T, dfo_T, dfh_T, dfl_T, dfv_T,on='RPOWER.NS')
        df_merge_col = [df_tik1[i], dfc_T[header2[i]], dfo_T[header2[i]], dfh_T[header2[i]], dfl_T[header2[i]], dfv_T[header2[i]], df_label[header2[i]],df_label5[header2[i]]]
        df_all =pd.concat(df_merge_col,axis=1)
        header1=["ticker","close","open","high", "low", "volume","label1","label5"]
        df_all.columns=header1
    
           
        #df_combine=df_combine.append(df_all.iloc[0:2300,:])
        #df_infer=df_infer.append(df_all.iloc[2300:2490,:])
        df_combine=pd.concat([df_combine,df_all])
    
    df_combine1=df_combine.dropna()
    df_combine1.reset_index(drop=True, inplace=True)
    df_combine1.to_csv(path+filename_out,index=False,header=True,mode ='w')
    
    return None
    #df_infer.to_csv('infer_training_2016_not_scale.csv',index=False,header=True,mode ='w')
    
    

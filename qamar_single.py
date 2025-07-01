#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 20:30:18 2020

@author: qamara
"""
def QI(path_qi,back_test,df_1,i):
    import pandas as pd
    import numpy as np
    import math
    import datetime
    import time
    from SP_market_fun_A import qamarIndex
    from functools import reduce
    #import sqlite3
    
    #today=time.strftime('%Y%m%d')
    #today = 20210307
    #conn = sqlite3.connect("qamar_index.db")
    #cur = conn.cursor()
    window_days = 6
    #path_qi = 'C:/Users/qamara/Desktop/test/data/'
    
    df_close ={}
    #df = pd.read_csv(path_qi+'/close.csv', header=None)
    df_1.drop(df_1.iloc[:, -back_test:], axis=1, inplace=True)
    kk=1
    #for kk in range(1,6):
    last_day=df_1.shape[1]-kk  
    df_close = qamarIndex(df_1,window_days,last_day)
    df_close.columns = ['Ticker',i]
        
        
    
    #df_m.to_sql("QAMAR_INDEX", conn, index=False, if_exists="replace")    
    #df_close1.to_sql("QAMAR_INDEX", conn, index=False, if_exists="replace")
    #df_test= pd.read_sql_query("select * from qamar_index WHERE (diff1>0 AND diff2>0 AND diff3>0 AND diff4>0) ORDER BY Mean DESC;", conn)
    #df_desc= pd.read_sql_query("SELECT * FROM qamar_index ORDER BY Mean DESC;", conn)
    #df_1.to_csv(path_qi+'QI.csv',index=True,header=False,mode ='w')

    return df_1,df_close
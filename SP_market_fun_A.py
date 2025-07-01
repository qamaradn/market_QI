# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 15:57:07 2020

@author: qamara
"""

def qamarIndex (df, window_days,last_day):

    import pandas as pd
    import numpy as np
    from numpy.linalg import eigh
    from numpy.linalg import inv
    from numpy import linalg as LA
    import datetime
    import time
      
    ep =0.000001
    comp_index = df.iloc[:,0].values.tolist()
    #last_day=df.shape[1]-1  # put number one less than yahoo pull data
    day_win=last_day-window_days
    next_day = last_day
    s=df.iloc[:,day_win:last_day+1].to_numpy().astype(float) #will generate one day less data
    s_next=df.iloc[:,next_day].to_numpy().astype(float)
    s=s[:,0::1]
    s_org=s
    #print(s_org)
    s = s - s.mean(axis=1,keepdims=True)
    s = s/(np.std(s,axis=1, keepdims=True)+ep)
    
    #np.random.shuffle(s)
    R = np.dot(s.transpose(),s)
    # Genrating eigen values and arranging in decreasing order (default output is increasing order by eigh)
    R_eval,R_evec = eigh(R)
    idx = R_eval.argsort()[::-1]   
    R_eval = R_eval[idx]
    R_evec = R_evec[:,idx]
    
    N=len(comp_index)
    # generating POD truncated series with first dominant eigen vector
    coff=R_evec[:,0].reshape(-1, 1)
    
    #si_re = s[0,:].reshape(-1, 1).transpose()
    pod_series=np.zeros((N))
    #test = s[1,:].reshape(-1, 1).transpose()
    
    for i in range(N):
        pod_series[i] = np.dot(s[i,:].reshape(-1, 1).transpose(),coff)
   
    grad=np.c_[np.array(comp_index),pod_series]
    df_grad = pd.DataFrame(data = grad)
    
    return df_grad
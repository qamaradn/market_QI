import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from numpy import absolute


def QIML(path,comp_num,testfile,label,algo,kk,k11):
    #path = 'Z:/AI_Test/AWS/qamar_index/data_train/'
    # Read the CSV file 
    train_df = pd.read_csv(path+'training_ratio.csv')
    #train_df = pd.read_csv("Z:/AI_Test/AWS/tests/MLJAR/0training_data.csv")
    #test_df = pd.read_csv(path+'testQI.csv')
    test_df = pd.read_csv(path+testfile)
    #test_df = pd.read_csv("Z:/AI_Test/AWS/tests/MLJAR/1training_data.csv")
    #print(train_df.head())
    #test_df=pd.concat([test_df]*2, ignore_index=True)
    
    #print(test_df)
    #comp_num=257

    X = train_df.iloc[:,1:6] #1:6 original
    y = train_df[label]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = comp_num, random_state = 42) #

    automl = AutoML(algorithms=[algo],golden_features=False)#(mode="Compete")
    #automl = AutoML()#(mode="Compete")
    automl.fit(X_train, y_train)

#-------------------------------------------------   
#    model = xgb.XGBRegressor( learning_rate=0.5)
#    # define model evaluation method
#    model.fit(X, y)
#    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
#    # evaluate model
#    scores = cross_val_score(model, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
#    # force scores to be positive
#    scores = absolute(scores)
#    print('Mean MAE: %.3f (%.3f)' % (scores.mean(), scores.std()) )
    
#    y_pred = model.predict(X_test)
#---------------------------------------------------
    y_pred= automl.predict(X_test)
    #yinfer = model.predict(X_infer)
    predictions = [round(value) for value in y_pred]
    #accuracy = accuracy_score(y_test, predictions)
    #print("Accuracy: %.2f%%" % (accuracy * 100.0))
    #print(y_test,y_pred)
    #kfold = KFold(n_splits=3, random_state=7)
    #results = cross_val_score(model, X, Y, cv=kfold)
    #print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
    #============================================================================x_GBOOST ENDS
    ######################################################
    collect=pd.DataFrame()
    #predictions=pd.DataFrame()
    num_rows=test_df.shape[0]
    print(num_rows)
    current_row=0
#    while current_row < len(test_df):
    extract_row=test_df[current_row:current_row+num_rows]
    X_pre = extract_row.iloc[:,1:6] #8:16 original
    X_p = extract_row.iloc[:,:] #8:16 original
        #y_pre = extract_row.iloc[:,6]
        #predictions=pd.DataFrame()
        #predictions= automl.predict(X_pre)
    #print(X_pre)
    if kk==1:
        predictions= automl.predict(X_pre)
        re_p= np.reshape(predictions,(num_rows,1)) 
    else:   
        predictions= automl.predict_all(X_pre)
        re=predictions['prediction_1'].to_numpy()
        re_p= np.reshape(re,(num_rows,1))
    #print(re_p.size)
        #predictions.columns=['Pre_label']
    combine=pd.DataFrame(np.concatenate((X_p,re_p),axis=1))
    
        #predictions = pd.concat((test_df[current_row:current_row+num_rows],predictions), axis=1)
    combine.columns=['0','close.csv','high.csv','open.csv','low.csv','volume.csv','label5','label1','Pre_label']
    combine=combine.sort_values(by = ['Pre_label'],ascending = False).reset_index(drop=True)
    combine_new=combine[combine['Pre_label'] >= 0.7]
    #print(combine_new.shape[0])
    combine_new.iloc[:,0:8].to_csv(path+testfile,header=True, index=False,mode='w')  #0:8
    combine.to_csv(path+str(k11)+'buy.csv',header=True, index=False,mode='w')  #0:8
    #print(combine)
        #predictions=predictions.sort_values(by = ['Pre_label'],ascending = False).reset_index(drop=True)
#        collect = pd.concat((collect,combine.head(1)), axis=0)
#        current_row +=num_rows
        

    return combine.iloc[0:6,[0,8]],combine_new.shape[0],combine.iloc[0,7]
    #return combine.shape[0]
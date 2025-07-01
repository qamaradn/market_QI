# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 08:12:45 2020
@author: Adnan Qamar, Water Desalination and Reuse Center, KAUST.
Email : Adnan.Qamar@kaust.edu.sa
"""
#def data_pulling():
#import math
#import datetime
import time
import os
#import datapackage
import pandas as pd
import yfinance as yf
#import numpy as np
#import os



#data = pd.read_csv('c:/Users/Adnan Qamar/Desktop/AWS/code_aws/data_live/s_p.csv',header=None)
data = pd.read_csv('c:/Users/Adnan Qamar/Desktop/AWS/code_aws/data_live/asx200.csv',header=None)

comp_index = data[0].values.tolist()   # using 6 for nifty_500 file

data2 = pd.DataFrame()
k=0
data1 ={}
for i in comp_index:
    
    
    try:
        
        msft = yf.Ticker(i)
        #data1[k] = msft.history(period="5d",interval ="1h")
        data1[k] = msft.history(period="1mo",interval ="30m")
        k=k+1    
        print(k,i)
    #except TypeError:
    except (KeyError, TypeError):
        k=k+1 
        pass  
        #except KeyError:
k=0
for l in comp_index:  
    if data1[k].shape[0] > 0:          
        data1[k]=data1[k].drop(data1[k].columns[[5,6]], axis=1) 
        data1[k].columns = [[l,l,l,l,l],['Open','High','Low','Close','Volume']]
        data2 = pd.concat([data2, data1[k]], axis=1)       
        k=k+1
        print(k)
    else:
        k=k+1
        
data2.to_csv('data1.csv',index=True,header=True,mode ='w')
#xp=data2.iloc[:, data2.columns.get_level_values(0)=='SUZLON.NS']
#xp.columns=xp.columns.droplevel(1)
# connection = mysql.connector.connect(user='', password='',
#                                          host='',port=3306,
#                                          database='');
#     cursor = connection.cursor()  # get the cursor
#     cursor.execute('')
#     extracted_data = cursor.fetchall();
#     for i in extracted_data:
#         print(i)
# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="yourusername",
#   password="yourpassword",
#   database="mydatabase"
# )
# mycursor = mydb.cursor()

# mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

# df = pd.read_csv('data.csv')

# df.to_sql('customers', con=mydb, if_exists='append', index=False)

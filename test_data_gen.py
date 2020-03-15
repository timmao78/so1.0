#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import os
import re
import numpy as np
import pandas as pd
import itertools
from datetime import datetime
from bsm_option_class import call_option, put_option
from so_func import get_exercise_time, get_T, get_empty_frame
from dateutil.relativedelta import relativedelta
import sqlalchemy


# In[2]:


def strptime_wrapper(string, fformat):
    return np.array(datetime.strptime(string, fformat))


# In[3]:


def get_EXP():
    """
    Return a list containing the months at which options that interest us expire.
    """
    today = datetime.today()
    if today <  get_exercise_time(today.year, today.month):
        exp1 = f"{str(today.year)[-2:]}{str(today.month).rjust(2,'0')}"
        exp2 = f"{str((today+relativedelta(months=1)).year)[-2:]}{str((today+relativedelta(months=1)).month).rjust(2,'0')}"
        EXP = [[exp1, exp2], [exp1, exp2]]
    else:
        exp1 = f"{str((today+relativedelta(months=1)).year)[-2:]}{str((today+relativedelta(months=1)).month).rjust(2,'0')}"
        exp2 = f"{str((today+relativedelta(months=2)).year)[-2:]}{str((today+relativedelta(months=2)).month).rjust(2,'0')}"
        EXP = [[exp1, exp2], [exp1, exp2]]
    return EXP


# In[4]:


def get_stk(CODE):
    engine = sqlalchemy.create_engine('mysql+pymysql://Tim:{}@localhost:3306/options'.format('123456'))

    df = pd.read_sql_table(table_name=CODE, con=engine, index_col='time')
    df.replace(0, np.nan, inplace=True)
    df.dropna(inplace=True)
    current_price = df.iloc[-1, 1]

    if current_price > 3:
        strike = int(current_price*1000) - int(current_price*1000)%100
    elif current_price < 3:
        strike = int(current_price*1000) - int(current_price*1000)%50
    else:
        strike = 3000

    strike_list = [strike]

    for i in range(2):
        if strike < 3000:
            strike = strike + 50
            strike_list.append(strike)
        else:
            strike = strike + 100
            strike_list.append(strike)

    strike = strike_list[0]

    for i in range(2):
        if strike <= 3000:
            strike = strike - 50
            strike_list.append(strike)
        else:
            strike = strike - 100
            strike_list.append(strike)

    output_list = []
    for _ in strike_list:
        output_list.append(str(_).rjust(5,'0'))

    return sorted(output_list)

def get_STK():
    return [get_stk('510050'), get_stk('510300')]


# In[5]:


today = datetime.today()
current_date = today.strftime('%Y-%m-%d')
source_txt = f"{current_date}.txt" 
# source_txt


# In[6]:


UNDL=[['510050'],['510300']]
# UNDL


# In[7]:


EXP = get_EXP()
# EXP


# In[8]:


STK = get_STK()
# STK


# In[9]:


zs = zip(UNDL, EXP, STK)


# In[10]:


options = []
code_call = []
code_put = []
for z in zs:
    prods = itertools.product(z[0], z[1], z[2])
    for prod in prods:
        options.append('_'.join(prod)) 
        code_call.append(prod[0]+'C'+prod[1]+'M'+prod[2])
        code_put.append(prod[0]+'P'+prod[1]+'M'+prod[2])


# In[11]:


df_underlyings = {}
for undl in UNDL:
    df = get_empty_frame()
    df.drop(columns=['C','P','nc','np','ivc', 'ivp', 'ir', 'ineq'], inplace=True)
    df_underlyings.update({undl[0]:df})


# In[12]:


df_options = {}
for option in options:    
    df = get_empty_frame()
    df.drop(columns=['S','n', 'ivc', 'ivp', 'ir', 'ineq'], inplace=True)
    current_time_object = (current_date + ' ' + df['time']).apply(strptime_wrapper, fformat = "%Y-%m-%d %H:%M")
    T = get_T(option[7:9], option[9:11], current_time_object)
    df['T'] = T
    df_options.update({option:df})


# In[13]:


df_underlyings['510050']['S'] = int(STK[0][2])/1000
df_underlyings['510300']['S'] = int(STK[1][2])/1000


# In[14]:


r = 0.025
sigma = 0.3
for option in df_options:
    sigma = sigma+0.01
    K = int(option[-5:])/1000
    
    oc = call_option(df_underlyings[option[:6]]['S'], K, df_options[option]['T'], r, sigma)
    df_options[option]['C'] = oc.value()
    
    op =  put_option(df_underlyings[option[:6]]['S'], K, df_options[option]['T'], r, sigma)
    df_options[option]['P'] = op.value()
    
    df_options[option].set_index('time', inplace=True)
    df_options[option].to_csv(f'{option}.csv')


# In[15]:


df_underlyings['510050'].set_index('time', inplace=True)
df_underlyings['510050'].to_csv('510050.csv')
df_underlyings['510300'].set_index('time', inplace=True)
df_underlyings['510300'].to_csv('510300.csv')


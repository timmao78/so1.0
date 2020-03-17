#! /Users/tianranmao/Projects/so1.0/venv/bin/python

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

    for i in range(3):
        if strike < 3000:
            strike = strike + 50
            strike_list.append(strike)
        else:
            strike = strike + 100
            strike_list.append(strike)

    strike = strike_list[0]

    for i in range(3):
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
source_txt = f"./txt/{current_date}.txt" 
csv_dir = f'./csv/{current_date}'
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)


# In[ ]:





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


def from_txt_to_csv(UNDL=None, EXP=None, STK=None, r=0.0275, sigma=0.2):
    last_size = 0
    last_read = 0
    pattern_code = re.compile('"code":"(\d+)",')
    pattern_time = re.compile('"time":(\d+),')
    
    while(True):
        time.sleep(3)
        if last_size != os.stat(source_txt).st_size:
            with open(source_txt, 'r') as rf:
                this_read = 0
                for line in rf:
                    this_read += 1
                    if this_read > last_read:  
                        last_read = this_read

                        match_code = re.search(pattern_code, line)
                        match_time = re.search(pattern_time, line)

                        if len(match_time.group(1))==5:
                            web_time = '0' + match_time.group(1)[-5:-4] + ':' + match_time.group(1)[-4:-2]  + ':' + match_time.group(1)[-2:]
                        else:
                            web_time = match_time.group(1)[-6:-4] + ':' + match_time.group(1)[-4:-2]  + ':' + match_time.group(1)[-2:]

                        if web_time[:-3] == '15:00':
                            
                            for underlying in df_underlyings:
                                underlying_write = df_underlyings[underlying].replace(0, np.nan)
                                underlying_write.set_index('time', inplace=True)
                                underlying_write.to_csv(f'{csv_dir}/{underlying}.csv')
                
                            for option in df_options:
                                option_write = df_options[option].replace(0, np.nan)
                                option_write.set_index('time', inplace=True)
                                option_write.to_csv(f'{csv_dir}/{option}.csv') 
                                
                            print('All done.')
                            
                            return None

                        if match_code!=None and match_code.group(1) in df_underlyings.keys():
                            print('\r',f'{web_time[:-3]}', end='')

                            pattern_price = re.compile('\[([\d]+),([\d.]+),([\d]+|null)\]')
                            match_price = re.findall(pattern_price, line)

                            i = df_underlyings[match_code.group(1)]['time']==web_time[:-3]

                            if sum(i)!=0 and float(match_price[-1][1])>0.001:
                                df_underlyings[match_code.group(1)].loc[i,'S'] = round((df_underlyings[match_code.group(1)].loc[i,'S']*df_underlyings[match_code.group(1)].loc[i,'n'] +float(match_price[-1][1]))/(df_underlyings[match_code.group(1)].loc[i,'n']+1),3)
                                df_underlyings[match_code.group(1)].loc[i,'n'] += 1

                        else:
                            pattern_price = re.compile('\[\"(510300[\d\w]+|510050[\d\w]+)\s+\",([\d.]+),[-\d.]+,[\d.]+,[\d.]+\]')
                            match_price = re.findall(pattern_price, line)

                            for e in match_price:
                                op_type = e[0][6]
                                key = e[0].replace('C','_')
                                key = key.replace('P','_')
                                key = key.replace('M','_')

                                if key in df_options.keys() and op_type=='C':
                                    K = float(key[-5:])/1000.0
                                    i = df_options[key]['time']==web_time[:-3]
                                    if sum(i)!=0 and float(e[1])>0.0001:
                                        option_price = (df_options[key].loc[i,'C']*df_options[key].loc[i,'nc'] +float(e[1]))/(df_options[key].loc[i,'nc']+1)
                                        df_options[key].loc[i,'C'] = round(option_price,4)
                                        df_options[key].loc[i,'nc'] += 1


                                elif key in df_options.keys():
                                    K = float(key[-5:])/1000.0
                                    i = df_options[key]['time']==web_time[:-3]
                                    if sum(i)!=0 and float(e[1])>0.0001:
                                        option_price = (df_options[key].loc[i,'P']*df_options[key].loc[i,'np'] +float(e[1]))/(df_options[key].loc[i,'np']+1)
                                        df_options[key].loc[i,'P'] = round(option_price,4)
                                        df_options[key].loc[i,'np'] += 1
                                        
            for underlying in df_underlyings:
                underlying_write = df_underlyings[underlying].replace(0, np.nan)
                underlying_write.set_index('time', inplace=True)
                underlying_write.to_csv(f'{csv_dir}/{underlying}.csv')

            for option in df_options:
                option_write = df_options[option].replace(0, np.nan)
                option_write.set_index('time', inplace=True)
                option_write.to_csv(f'{csv_dir}/{option}.csv')
                
            last_size = os.stat(source_txt).st_size  


# In[14]:


from_txt_to_csv(UNDL=UNDL, EXP=EXP, STK=STK)


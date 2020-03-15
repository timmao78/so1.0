from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def get_exercise_time(exercise_year, exercise_month): 
    """
    Returns the time of the 3:00 pm, third Wednesday of the given month.
    """
    if int(exercise_year) < 1000:
        dt = datetime.strptime('{} {}'.format(exercise_year, exercise_month), '%y %m')
    else:
        dt = datetime.strptime('{} {}'.format(exercise_year, exercise_month), '%Y %m')
        
    #shanghai_tz = pytz.timezone('Asia/Shanghai')  # shanghai_tz is a timezone
    #dt = shanghai_tz.localize(dt)
    
    if dt.weekday() == 2:
        return dt + timedelta(days=21) + timedelta(hours=15)
    elif dt.weekday() < 2:
        return dt + timedelta(days=23-dt.weekday()) + timedelta(hours=15)
    else:
        return dt + timedelta(days=30-dt.weekday()) + timedelta(hours=15)

def get_T(exercise_year, exercise_month, current_time_object):
    """
    Return total time(in years) until expiration.
    """
    T = get_exercise_time(exercise_year, exercise_month) - current_time_object
    return T.apply(lambda x: round(x.total_seconds()/(365*24*3600), 5))


def get_time():
    time = []
    for hours in range(9,15):
        for minutes in range(60):
            if (hours==9 and minutes>=30) or hours==10 or hours==13 or hours==14 or (hours==11 and minutes<30):
                time.append('{:0>2d}:{:0>2d}'.format(hours,minutes))
    return time

def get_empty_frame():
    return pd.DataFrame({'time':get_time(), 'C':0, 'P':0, 'S':0, 'n':0, 'nc':0, 'np':0, 'ivc':0, 'ivp':0, 'ir':0, 'ineq':0})


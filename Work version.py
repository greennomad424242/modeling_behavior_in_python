
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 19:56:46 2016
 
@author: matthowes
"""
 
import matplotlib.pyplot as plt
from pylab import * 
import math
import random 
import datetime
import pandas as pd

def schedule(time_sleep_index):
    
    return {
        1: datetime.datetime(2016, 1, day_setup, 20, 15 ),   
        2: datetime.datetime(2016, 1, day_setup, 20, 45 ),     
        3: datetime.datetime(2016, 1, day_setup, 21, 15 ),   
        4: datetime.datetime(2016, 1, day_setup, 22, 00 )
    }.get(time_sleep_index)
 
#def fatigue(K,x,x0,L):
 #   xd = L / (1 + math.exp(-K*(x-x0-9))) 
 #   if awake_status =='asleep':
 #       xd = 0
 #   return xd

# configuration parameters    
    
L = 1
K = 0.5
x0 = 0    
        
# variable setting 

hours_awake= 0
hours_asleep = 0 
time_increment = 0.25
df_day_schedule = pd.DataFrame(columns=['event_date','wake_time','sleep_time'])
df_hourly_status = pd.DataFrame(columns=['time','awake_status','hours_awake','fatigue'])

for day_setup in range(1,12): 
     time_sleep_index = random.randint(1, 4)
     df_day_schedule = df_day_schedule.append(pd.Series([datetime.datetime(2016, 1, day_setup), 
                                                         datetime.datetime(2016, 1, day_setup, 5, 0),  
                                                         schedule(time_sleep_index)], 
                                            index=['event_date','wake_time','sleep_time']), ignore_index=True)

# initial conditions 

current_time =  datetime.datetime(2016, 1, 1, 1, 0 )
awake_status = 'asleep'


 
#print (df_day_schedule[df_day_schedule.date.day == current_time.day])

for x in range(1,140):
   date_stamp = current_time.date()   
  
   current_time =  current_time + datetime.timedelta(hours=time_increment)
   
   if current_time.date() != date_stamp or x==1:  # get wake_time
        wake_time_numpy = df_day_schedule[df_day_schedule['event_date'] == current_time.date()].wake_time.values[0]
        wake_time = datetime.datetime.utcfromtimestamp(wake_time_numpy.tolist()/1e9)                            
        sleep_time_numpy = df_day_schedule[df_day_schedule['event_date'] == current_time.date()].sleep_time.values[0]
        sleep_time = datetime.datetime.utcfromtimestamp(sleep_time_numpy.tolist()/1e9)                              
            
   if current_time >= wake_time and current_time < sleep_time and awake_status =='asleep': #if time to get up
        awake_status ="awake"
        prev_night_sleep = hours_asleep
        hours_awake = 0
        hours_asleep = 0
   elif current_time >= sleep_time and awake_status =='awake':  # if bedtime   
        awake_status ="asleep"
        hours_asleep = 0
        hours_awake = 0
   elif awake_status =='awake':
       hours_awake += time_increment  
       fatigue += awake_fatigue_increment  
   else:
       hours_asleep += time_increment 
       fatigue -= asleep_fatigue_decrement      
    
   df_hourly_status = df_hourly_status.append(pd.Series([current_time,awake_status, hours_awake,fatigue ], 
                                                        index=['time','awake_status','hours_awake', 'fatigue']), ignore_index=True)
   


with pd.option_context('display.max_rows', 999, 'display.max_columns', 6):
    print(df_hourly_status)   
df_hourly_status.plot(x='time', y=['fatigue'])
    # 

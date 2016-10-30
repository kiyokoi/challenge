# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

# Load Data

df01 = pd.read_csv('201501-citibike-tripdata.csv')
df02 = pd.read_csv('201502-citibike-tripdata.csv')
df03 = pd.read_csv('201503-citibike-tripdata.csv')
df04 = pd.read_csv('201504-citibike-tripdata.csv')
df05 = pd.read_csv('201505-citibike-tripdata.csv')
df06 = pd.read_csv('201506-citibike-tripdata.csv')
df07 = pd.read_csv('201507-citibike-tripdata.csv')
df08 = pd.read_csv('201508-citibike-tripdata.csv')
df09 = pd.read_csv('201509-citibike-tripdata.csv')
df10 = pd.read_csv('201510-citibike-tripdata.csv')
df11 = pd.read_csv('201511-citibike-tripdata.csv')
df12 = pd.read_csv('201512-citibike-tripdata.csv')

need_seconds = [df01, df02, df03, df06]
for df in need_seconds:
    df['starttime'] = df['starttime'] + ':00'
    df['stoptime'] = df['stoptime'] + ':00'

df = pd.DataFrame()
df_list = [df01, df02, df03, df04, df05,
           df06, df07, df08, df09, df10, df11, df12]
for files in df_list:
    df = df.append(files)

# Trip Duration

df['starttime'] = pd.to_datetime(df['starttime'], format='%m/%d/%Y %H:%M:%S')
df['stoptime'] = pd.to_datetime(df['stoptime'], format='%m/%d/%Y %H:%M:%S')
#df['diff'] = (df['stoptime'] - df['starttime']) / np.timedelta64(1, 's')

print df['tripduration'].median()   # 629.0

# fraction start end at same station

df['same_station'] = df['start station id'] == df['end station id']
print df['same_station'][df['same_station'] == True].sum() / float(df.shape[0])
    # 0.0223583913373


# standard deviation of the number of station visited by a bike

df_renamed = df.rename(columns={'start station id': 'start_station_id',
                                'end station id': 'end_station_id'}, inplace=True)
start_stations = pd.DataFrame({'stations': df.groupby(
    'bikeid').start_station_id.apply(list)}).reset_index()
end_stations = pd.DataFrame({'stations': df.groupby(
    'bikeid').end_station_id.apply(list)}).reset_index()
print start_stations.shape  # (8477, 2)
print end_stations.shape  # (8477, 2)

stations = pd.merge(start_stations, end_stations, on='bikeid')
stations['stations'] = stations['stations_x'] + stations['stations_y']

unique = []
for index, row in stations.iterrows():
    unique.append(len(set(row['stations'])))
print np.std(unique)    # 54.5418965359


# average trip length in km

dfd = df.loc[(df['end station latitude'] > df['start station latitude']) & (
    df['end station longitude'] > df['start station longitude'])]

from math import cos, sin, acos, pi


def distance(lon_start, lat_start, lon_end, lat_end):
    degrees_to_radians = pi / 180.0
    phi1 = (90.0 - lat_start) * degrees_to_radians
    phi2 = (90.0 - lat_end) * degrees_to_radians
    theta1 = lon_start * degrees_to_radians
    theta2 = lon_end * degrees_to_radians

    cosine = (sin(phi1) * sin(phi2) *
              cos(theta1 - theta2) + cos(phi1) * cos(phi2))
    km = acos(cosine) * 6373
    return km

dfd['distance'] = map(distance, dfd['start station longitude'], dfd[
                      'start station latitude'], dfd['end station longitude'], dfd['end station latitude'])

print dfd['distance'].mean()  # 1.9390509269 km


# max - min monthly ave duration

monthly_ave = []
for files in df_list:
    monthly_ave.append(files['tripduration'].mean())

print max(monthly_ave) - min(monthly_ave)  # 430.57029597

'''
month - monthly average(s)
11 - 972.175200685
10 - 1080.14148582
12 - 946.210875175
02 - 649.391763571
03 - 734.625160169
01 - 654.34589847
06 - 905.082366591
07 - 968.169149912
04 - 930.366569077
05 - 1000.73166865
08 - 1017.97768192
09 - 1051.349442
'''

# fraction exceeded time limit

df['exceed'] = ((df['usertype'] == 'Customer') & (df['tripduration'] > 1800.0)) | (
    (df['usertype'] == 'Subscriber') & (df['tripduration'] > 2700.0))
print df['exceed'][df['exceed'] == True].sum() / float(df.shape[0])
    # 0.0381067801681


# average bike move per bike

dfa = df.sort(['bikeid', 'starttime'])
dfa['start station id'] = dfa['start station id'].shift(-1)
dfa['start bikeid'] = dfa['bikeid'].shift(-1)

dfa['removed'] = (dfa['bikeid'] == dfa['start bikeid']) & (
    dfa['end station id'] != dfa['start station id'])
print dfa['removed'][dfa['removed'] == True].sum() / float(len(dfa['bikeid'].unique()))
    # 65.4249144745 per bike

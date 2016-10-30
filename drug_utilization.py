# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 08:10:00 2016

@author: Kiyoko
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

iter_05 = pd.read_csv('State_Drug_Utilization_Data_2005.csv',
                      iterator=True, chunksize=5000)
df05 = pd.concat([chunk[(chunk['Suppression Used'] == False)
                        & (chunk['State'] != 'XX')] for chunk in iter_05])
print df05.shape  # (1291403, 20)

iter_07 = pd.read_csv('State_Drug_Utilization_Data_2007.csv',
                      iterator=True, chunksize=5000)
df07 = pd.concat([chunk[(chunk['Suppression Used'] == False)
                        & (chunk['State'] != 'XX')] for chunk in iter_07])
print df07.shape  # (979286, 20)

iter_09 = pd.read_csv('State_Drug_Utilization_Data_2009.csv',
                      iterator=True, chunksize=5000)
df09 = pd.concat([chunk[(chunk['Suppression Used'] == False)
                        & (chunk['State'] != 'XX')] for chunk in iter_09])
print df09.shape  # (1085318, 20)

iter_11 = pd.read_csv('State_Drug_Utilization_Data_2011.csv',
                      iterator=True, chunksize=5000)
df11 = pd.concat([chunk[(chunk['Suppression Used'] == False)
                        & (chunk['State'] != 'XX')] for chunk in iter_11])
print df11.shape  # (1596407, 20)

iter_13 = pd.read_csv('State_Drug_Utilization_Data_2013.csv',
                      iterator=True, chunksize=5000)
df13 = pd.concat([chunk[(chunk['Suppression Used'] == False)
                        & (chunk['State'] != 'XX')] for chunk in iter_13])
print df13.shape  # (1802170, 20)

iter_15 = pd.read_csv('State_Drug_Utilization_Data_2015.csv',
                      iterator=True, chunksize=5000)
df15 = pd.concat([chunk[(chunk['Suppression Used'] == False)
                        & (chunk['State'] != 'XX')] for chunk in iter_15])
print df15.shape  # (1983852, 20)


# select top 10 reimbursed value
group = df15.groupby('Product Name').agg({'Total Amount Reimbursed': sum}).sort_values(
    by='Total Amount Reimbursed', ascending=False)
group = group.head(10)
print group.index
top10 = ['HARVONI 90', 'METHYLPHEN', 'ABILIFY', 'SOVALDI 40', 'LANTUS 3ML',
         'ARIPIPRAZO', 'HUMIRA 40', 'TRUVADA 20', 'ADDERALL X', 'LANTUS 100']

# select the same top10
df15_top10 = df15.loc[df15['Product Name'].isin(top10)]
df13_top10 = df13.loc[df13['Product Name'].isin(top10)]
df11_top10 = df11.loc[df11['Product Name'].isin(top10)]
df09_top10 = df09.loc[df09['Product Name'].isin(top10)]
df07_top10 = df07.loc[df07['Product Name'].isin(top10)]
df05_top10 = df05.loc[df05['Product Name'].isin(top10)]

df_top10 = pd.DataFrame()
df_list_top10 = [df05_top10, df07_top10,
                 df09_top10, df11_top10, df13_top10, df15_top10]
for data in df_list_top10:
    df_top10 = df_top10.append(data)

print df_top10.shape  # (53409, 20)

df_total_reimbursed = df_top10.groupby(['Product Name', 'Year']).sum()[
    ['Total Amount Reimbursed']].reset_index()
df_total_reimbursed.head()

plt.xticks(rotation=40)
plt.xlabel('Product Name with 10 Most Reimbursement in 2015')
plt.title('Total Amount Reimbursed by Drug ($Billion)')
sns.barplot(x='Product Name', y='Total Amount Reimbursed',
            hue='Year', data=df_total_reimbursed)
plt.savefig('top10_2015.png')


# total expenditure by year
df15_exp = df15[['Year', 'Total Amount Reimbursed']]
df13_exp = df13[['Year', 'Total Amount Reimbursed']]
df11_exp = df11[['Year', 'Total Amount Reimbursed']]
df09_exp = df09[['Year', 'Total Amount Reimbursed']]
df07_exp = df07[['Year', 'Total Amount Reimbursed']]
df05_exp = df05[['Year', 'Total Amount Reimbursed']]

df_exp = pd.DataFrame()
df_list_exp = [df05_exp, df07_exp, df09_exp, df11_exp, df13_exp, df15_exp]
for data in df_list_exp:
    df_exp = df_exp.append(data)

print df_exp.shape  # (9561880, 2)

df_total_reimbursed2 = df_exp.groupby(
    'Year').sum()[['Total Amount Reimbursed']].reset_index()
df_total_reimbursed2.head()

plt.xticks(rotation=40)
plt.title('Total Amount Reimbursed by Year ($100 billion)')
sns.barplot(x='Year', y='Total Amount Reimbursed', data=df_total_reimbursed2)
plt.savefig('total_expenditure.png')


# total expenditure by location
df15_loc = df15[['Year', 'Total Amount Reimbursed', 'Latitude', 'Longitude']]
df13_loc = df13[['Year', 'Total Amount Reimbursed', 'Latitude', 'Longitude']]
df11_loc = df11[['Year', 'Total Amount Reimbursed', 'Latitude', 'Longitude']]
df09_loc = df09[['Year', 'Total Amount Reimbursed', 'Latitude', 'Longitude']]
df07_loc = df07[['Year', 'Total Amount Reimbursed', 'Latitude', 'Longitude']]
df05_loc = df05[['Year', 'Total Amount Reimbursed', 'Latitude', 'Longitude']]

df15_loc_total = df15_loc.groupby(['Latitude', 'Longitude']).sum()[
    ['Total Amount Reimbursed']].reset_index()
df05_loc_total = df05_loc.groupby(['Latitude', 'Longitude']).sum()[
    ['Total Amount Reimbursed']].reset_index()

plt.figure(figsize=(20, 10))
img = plt.imread('Geo-map-USA-contour.png')
imgplot = plt.imshow(img, interpolation='bilinear',
                     origin='upper', extent=[-126, -66, 25, 49.5])
plt.scatter(df15_loc_total['Longitude'], df15_loc_total['Latitude'], s=df15_loc_total[
            'Total Amount Reimbursed'] / 20000000, edgecolors='b', facecolors='None')
plt.scatter(df05_loc_total['Longitude'], df05_loc_total['Latitude'], s=df05_loc_total[
            'Total Amount Reimbursed'] / 20000000, edgecolors='r', facecolors='None')
plt.xlim([-126, -66])
plt.ylim([25, 49.5])
plt.savefig('state_2015.png')


# investigate high reimbursement in TN in 2005

df05_sorted = df05.sort_values(by='Total Amount Reimbursed', ascending=False)
# number of highest reimbursement amount from TN
print df05_sorted.head(250)['State'].unique()    # ['TN']
# inspect top 10 highest reimbursement amount
print df05_sorted.head(10)[['State', 'Product Name', 'Number of Prescriptions', 'Total Amount Reimbursed']]

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 18:43:21 2023

@author: Georg
"""

import WorldBankParser as WBP
import pandas as pd
import matplotlib.pyplot as plt

c02_df, c02_df_tr = WBP.getDfs("C02PerCapita.csv")
current_df, current_df_tr = WBP.getDfs("CurrentAccount.csv")

fig, ax = plt.subplots()

year = '2015'

current_df_tr = current_df_tr.fillna(0)
c02_df_tr = c02_df_tr.fillna(0)
mask = (current_df_tr.loc[year] !=  0) & (c02_df_tr.loc[year] >=  1)

temp = pd.DataFrame(current_df_tr.loc[year][mask])
temp['Current Account'] = temp[year]
temp = temp.drop(year, axis = 1)
temp['C02'] = c02_df_tr.loc[year][mask]
print(temp.corr())

ax.scatter(current_df_tr.loc[year][mask], c02_df_tr.loc[year][mask], s = 1)
plt.axvline(0, color = 'black')
plt.xlabel('Current account balance (% of GDP)')
plt.ylabel('CO2 emissions (metric tons per capita)')
plt.title('Current Account Against C02 Emissions For Countries in {}'.format(year))

corrs = []
years = []

for i in range(1995, 2020):
    year = str(i)
    current_df_tr = current_df_tr.fillna(0)
    c02_df_tr = c02_df_tr.fillna(0)
    mask = (current_df_tr.loc[year] !=  0) & (c02_df_tr.loc[year] >=  1)
    
    temp = pd.DataFrame(current_df_tr.loc[year][mask])
    temp['Current Account'] = temp[year]
    temp = temp.drop(year, axis = 1)
    temp['C02'] = c02_df_tr.loc[year][mask]
    corrs.append(temp.corr().iloc[0,1])
    years.append(i)
    
fig, ax = plt.subplots()

ax.plot(years, corrs)
plt.ylim(0, 1)
plt.xlabel('Year')
plt.ylabel('Correlation Coefficient')
plt.title('Correlation Between Current Account and C02 Emissions per Capita')

    
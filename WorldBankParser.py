# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 14:07:25 2023

@author: Georg
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def getDfs(filename):
    
    temp_df = pd.read_csv(filename, skiprows = 4)
    
    temp_df_tr = pd.DataFrame(temp_df)
    temp_df_tr = temp_df_tr.transpose()
    temp_df_tr.columns = list(temp_df_tr.loc['Country Name',:])
    temp_df_tr = temp_df_tr.drop(['Country Name', 
                                  'Country Code',
                                  'Indicator Name',
                                  'Indicator Code'])
    
    return temp_df, temp_df_tr

# =============================================================================
# top_df, top_df_tr = getDfs('Top.csv')
# second_df, second_df_tr = getDfs('Second.csv')
# third_df, third_df_tr = getDfs('Third.csv')
# fourth_df, fourth_df_tr = getDfs('Fourth.csv')
# fifth_df, fifth_df_tr = getDfs('Fifth.csv')
# 
# new_index = pd.MultiIndex([[], []],
#                           [[], []],
#                           names = ['Country', 'Quintile'])
# 
# test = pd.DataFrame(columns = top_df_tr.index, index = new_index)
# 
# dfs = [top_df, second_df, third_df, fourth_df, fifth_df]
# labels = ['Top', 'Second', 'Third', 'Fourth', 'Fifth']
# G7 = ['France', 'Germany', 'United Kingdom']
# colours = ['black', 'blue', 'orange', 'red', 'yellow']
# 
# for country in G7:
#     for i, n in enumerate(dfs):
#         test.loc[(country, labels[i]),:] = n[n['Country Name'] == country].iloc[:, 4:].squeeze()
#         
# test = test.dropna(axis = 1)
# 
# fig, ax = plt.subplots()
# 
# labels.reverse()
# 
# for country in G7:
#     bottom = 0
#     for i, quintile in enumerate(labels):
#         ax.bar(country, test.loc[(country, quintile), '2013'],
#                bottom = bottom, 
#                label = quintile,
#                color = colours[i])
#         bottom += test.loc[(country, quintile), '2013']
#      
# fig, ax = plt.subplots()    
# 
# for year in test.columns:
#     bottom = 0
#     for i, quintile in enumerate(labels):
#         ax.bar(year, test.loc[('United Kingdom', quintile), year],
#                bottom = bottom, 
#                label = quintile,
#                color = colours[i])
#         bottom += test.loc[(country, quintile), year]
#         
# plt.xticks(rotation = 45)
# =============================================================================


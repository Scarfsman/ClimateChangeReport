# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:19:06 2023

@author: Georg
"""

import pandas as pd
export_df = pd.DataFrame(columns = ['Country', 'Exports', 'GDP'])

def getfigures(country, file):
    temp_df = pd.read_csv(file)
    x = {}
    x['Country'] = country
    x['Exports'] = temp_df[temp_df['Indicator'] == 'Exports (in US$ Mil)']['Indicator Value'].iloc[0]
    x['GDP'] = temp_df[temp_df['Indicator'] == 'GDP (current US$ Mil)']['Indicator Value'].iloc[0]
    temp_df = pd.DataFrame(x, index=[0])
    global export_df
    export_df = pd.concat([export_df, temp_df])
    
getfigures('China', 'en_CHN_at-a-glance.csv')


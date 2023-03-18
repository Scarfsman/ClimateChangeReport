# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 14:07:25 2023

@author: Georg
"""

import pandas as pd

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

c02_df, c02_df_tr = getDfs(r'API_EG.ELC.ACCS.ZS_DS2_en_csv_v2_4902219.csv')

emissions_df, emissions_df_tr = getDfs('co2emissions.csv')
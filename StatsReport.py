#%%
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 18:43:21 2023

@author: Georg
"""

import WorldBankParser as WBP
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('default')

#Import the dataframes of interest
c02_df, c02_df_tr = WBP.getDfs("C02PerCapita.csv")
current_df, current_df_tr = WBP.getDfs("CurrentAccount.csv")
gdp_df, gdp_df_tr = WBP.getDfs('GDPPerCapita.csv')
renew_df, renew_df_tr = WBP.getDfs('renewable.csv')

#import import databases
manu_df, manu_df_tr = WBP.getDfs('imports/Manufactures.csv')
ores_df, ores_df_tr = WBP.getDfs('imports/Ores.csv')
food_df, food_df_tr = WBP.getDfs('imports/Food.csv')
agri_df, agri_df_tr = WBP.getDfs('imports/Agriculture.csv')

#import economy databases
econ_m_df, econ_m_df_tr = WBP.getDfs('economy/Manufacturing.csv')
econ_i_df, econ_i_df_tr = WBP.getDfs('economy/Industry.csv')
econ_a_df, econ_a_df_tr = WBP.getDfs('economy/Agriculture.csv')
econ_s_df, econ_s_df_tr = WBP.getDfs('economy/Services.csv')

#Define our functions
def buildDataForLabel(dataframes, columns, lab):
    """
    

    Parameters
    ----------
    dataframes : list[pd.DataFrames]
        The dataframes for the variables. use _df for countries and _df_tr for years
    cols : list[str()]
        The variable names. The ith name corresponds to the ith dataframe
    labels : str()
        The label to pull from the dataframe. Pass a list of either all country names or all years
    Returns
    -------
    temp : pd.DataFrame
        the 

    """
    lab = str(lab)
    for i in range(len(dataframes)):
        dataframes[i] = dataframes[i].fillna(0)
    
    mask = []
    for i in range(dataframes[0].shape[1]):
        ith = True
        for  dataframe in dataframes:
            if dataframe.loc[lab].iloc[i] == 0:
                ith = False
        mask.append(ith)
    
    temp = pd.DataFrame(dataframes[0].loc[lab][mask])
    temp[columns[0]] = temp[lab]
    temp = temp.drop(lab, axis = 1)
    for i in range(1, len(dataframes)):
        temp[columns[i]] = dataframes[i].loc[lab][mask]
        
    return temp

def compareLabels(dataframes, cols, labels):
    """
    Builds a correlation matrix for the variables compiled in the passed dataframes for the labels 
    chosen. shows the correlation for the final variable in the list

    Parameters
    ----------
    dataframes : list[pd.DataFrames]
        The dataframes for the variables. use _df for countries and _df_tr for years
    cols : list[str()]
        The variable names. The ith name corresponds to the ith dataframe
    labels : list[str()]
        The labels to compare. Pass a list of either all country names or all years

    Returns
    -------
    temp_corr : pd.DataFrame
        returns the correlation of the variable against the variable in the last column
        for all the labels passed to the function.

    """
    new_data = []
    for i in labels:
        new_data.append(buildDataForLabel(dataframes, cols, i).corr())
        
    temp_corr = pd.DataFrame(new_data[0].iloc[:,len(cols) -1])
    a = cols[-1] 
    temp_corr[labels[0]] = temp_corr[a]
    temp_corr = temp_corr.drop(columns[-1], axis = 1)
    
    for i in range(1, len(labels)):
        temp_corr[labels[i]] = new_data[i].iloc[:,len(labels)-1]
        
    return temp_corr

def plotEconomies(labels):
    
    fig, ax = plt.subplots()

    cols = ['Manufacturing GDP', 'Industry GDP', 'Agriculture GDP', 'Services GDP']
    colours = ['#4B0082', '#9400D3', '#999900', '#CCCC00']

    N = len(labels)
    ind = np.arange(N) 
    print(ind)
    width = 0.25
    
    for nth, label in enumerate(labels):
        data = [econ_m_df, econ_i_df, econ_a_df, econ_s_df, gdp_df]
        columns = ['Manufacturing', 'Industry', 'Agriculture', 'Services', 'GDP']
        temp = buildDataForLabel(data, columns, label)
        temp['Manufacturing GDP'] = (temp['Manufacturing']*temp['GDP'])/100
        temp['Industry GDP'] = (temp['Industry']*temp['GDP'])/100
        temp['Agriculture GDP'] = (temp['Agriculture']*temp['GDP'])/100
        temp['Services GDP'] = (temp['Services']*temp['GDP'])/100
        
        #Get the values for the years of interest
        temp = temp.loc[['1995', '2015']]
        
        #Index the values based on the countires GDP in 1995
        indexer = temp.loc['1995', ['Manufacturing GDP', 'Industry GDP', 'Agriculture GDP', 'Services GDP']].sum()
        temp['Manufacturing GDP'] =  temp['Manufacturing GDP']/indexer
        temp['Industry GDP'] = temp['Industry GDP']/indexer
        temp['Agriculture GDP'] = temp['Agriculture GDP']/indexer
        temp['Services GDP'] = temp['Services GDP']/indexer
    
        #Create the bar for 1995
        bottom = 0
        for n, i in enumerate(cols):
            #stack the boxes for each sector of the economy
            ax.bar(ind[nth]-(width/2), temp[i].iloc[0], width, color = colours[n], bottom = bottom)
            bottom += temp[i].iloc[0]
            
        #Create the bar for 2015
        bottom = 0
        for n, i in enumerate(cols):
            #Create the bar for 1995
            ax.bar(ind[nth]+(width/2), temp[i].iloc[1], width, color = colours[n], bottom = bottom)
            bottom += temp[i].iloc[1]

    plt.xticks(ind, 
               labels, 
               fontsize = 'small')
    plt.title('Components of GDP By Sector 1995 Vs. 2015')
    plt.xlabel('Country')
    plt.ylabel('GDP Per Capita')
    ax.legend(['Manufacturing', 'Industry', 'Agriculture', 'Services'],
              loc='center left', 
              bbox_to_anchor=(1, 0.75))

def plotCO2(labels): 
    fig, ax = plt.subplots()
    x = [year for year in range(1995, 2016)]
    for i in labels:
        y = [c02_df_tr.loc[str(year), i] for year in x]
        ax.plot(x, y, label = i)
        
    plt.ylim(bottom = 0)
    plt.legend(loc='center left', 
               bbox_to_anchor=(1, 0.75))
    plt.show()
        

#%%
data = [current_df_tr, c02_df_tr, gdp_df_tr] 
labels = ['Current Account', 'C02', 'GDP']
corr_df = buildDataForLabel(data, labels, 2015)

fig, ax = plt.subplots()

ax.scatter(corr_df.loc[:,'Current Account'], corr_df.loc[:,'C02'], s = 1)
plt.axvline(0, color = 'black')
plt.xlabel('Current account balance (% of GDP)')
plt.ylabel('CO2 emissions (metric tons per capita)')
plt.title('Current Account Against C02 Emissions For Countries in {}'.format(2015))

#%%
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

#%%

data = [manu_df_tr, ores_df_tr, food_df_tr, agri_df_tr, current_df_tr, c02_df_tr]
labels = ['Manufactured', 'Ores', 'Food', 'Agriculture', 'Current Account', 'C02 Per Capita']
import_1995_df = buildDataForLabel(data, labels, 1995)

data = [econ_m_df_tr, econ_i_df_tr, econ_a_df_tr, econ_s_df_tr, gdp_df_tr, c02_df_tr]
labels = ['Manufacturing', 'Industry', 'Agriculture', 'Services', 'GDP','C02 Per Capita']
economy_2015_df = buildDataForLabel(data, labels, 1995)


#%%

data = [econ_m_df, econ_i_df, econ_a_df, econ_s_df, gdp_df, renew_df, c02_df]
columns = ['Manufacturing', 'Industry', 'Agriculture', 'Services', 'GDP', 'Renewables', 'C02 Per Capita']
labels = ['United Kingdom', 'United States', 'France', 'Germany', 'Japan', 'Italy', 'Canada']
all_corr = compareLabels(data, columns, labels)



#%%

economies = ['United Kingdom', 'Australia', 'Japan', 'India', 'Brazil', 'Germany']
plotEconomies(economies)
plotCO2(economies)

#%%


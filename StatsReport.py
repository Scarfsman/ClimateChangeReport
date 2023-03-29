#%%
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 18:43:21 2023

@author: Georg
"""
#import packages
import WorldBankParser as WBP
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

#Define our functions


def getDfs(filename):
    """
    Parameters
    ----------
    dataframes : str()
        The wordbank dataset in CSV format to be read into the script
    Returns
    -------
    temp_df : pd.DataFrame
        The world bank data frame read in the script with countries as rows and
        years as columns
    temp_df_tr : pd.DataFrame
        The world bank data frame read in the script with years as rows and
        countries as columns
    """
    #skip the rows with no useful information
    temp_df = pd.read_csv(filename, skiprows = 4)
    
    temp_df_tr = pd.DataFrame(temp_df)
    temp_df_tr = temp_df_tr.transpose()
    temp_df_tr.columns = list(temp_df_tr.loc['Country Name',:])
    #clean up the transposed dataframe by dropping the wors that aren't of 
    #interest
    temp_df_tr = temp_df_tr.drop(['Country Name', 
                                  'Country Code',
                                  'Indicator Name',
                                  'Indicator Code'])
    
    #clean up the untrasnposed dataframe. this is so that both dataframes can
    #be passed to the functions defined below
    temp_df = temp_df.set_index('Country Name', drop = True)
    temp_df = temp_df.drop(['Country Code',
                            'Indicator Name',
                            'Indicator Code'],
                             axis = 1)
    
    return temp_df, temp_df_tr


def buildDataForLabel(dataframes, columns, lab):
    """
    Parameters
    ----------
    dataframes : list[pd.DataFrames]
        The dataframes for the variables. use _df for countries and 
        _df_tr for years
    cols : list[str()]
        The variable names. The ith name corresponds to the ith dataframe
    labels : str()
        The label to pull from the dataframe. Pass a list of either all 
        country names or all years
    Returns
    -------
    temp : pd.DataFrame
        Returns a dataframe containing the information in the dataframes passed
        to the function for the label passed in lab
    """
    lab = str(lab)
    for i in range(len(dataframes)):
        dataframes[i] = dataframes[i].fillna(0)
    
    #Generate a boolean mask, so that the dataframe only contains information
    #for the variables where it is present for all values, e.g. if we pass a 
    #country as lab, and one of the variables is missing data for 1967, then 
    #1967 will be omitted for all vairables
    mask = []
    for i in range(dataframes[0].shape[1]):
        ith = True
        for  dataframe in dataframes:
            if dataframe.loc[lab].iloc[i] == 0:
                ith = False
        mask.append(ith)
    
    #initialise the dataframe by setting the first column equal to the data 
    #in the first dataframe, then clean it up
    temp = pd.DataFrame(dataframes[0].loc[lab][mask])
    temp[columns[0]] = temp[lab]
    temp = temp.drop(lab, axis = 1)
    
    #iterate through the rest of the dataframes in order to pull the values 
    #our target label
    for i in range(1, len(dataframes)):
        temp[columns[i]] = dataframes[i].loc[lab][mask]
        
    return temp


def compareLabels(dataframes, cols, labels):
    """
    Parameters
    ----------
    dataframes : list[pd.DataFrames]
        The dataframes for the variables. use _df for countries and _df_tr for 
        years
    cols : list[str()]
        The variable names. The ith name corresponds to the ith dataframe
    labels : list[str()]
        The labels to compare. Pass a list of either all country names or all 
        years

    Returns
    -------
    temp_corr : pd.DataFrame
        Returns the correlation of the variable against the variable in the 
        last column for all the labels passed to the function.
    """
    #build a list of dataframes for the labels and data we want to compare
    new_data = []
    for i in labels:
        new_data.append(buildDataForLabel(dataframes, cols, i).corr())
    
    #get the last column of the correlation matrix of the first dataset,
    #then intialise a dataframe with that data
    temp_corr = pd.DataFrame(new_data[0].iloc[:,len(cols) -1])
    a = cols[-1] 
    temp_corr[labels[0]] = temp_corr[a]
    temp_corr = temp_corr.drop(columns[-1], axis = 1)
    
    #iterate through the rest of the datasets and add the data for the rest
    #of the labels
    for i in range(1, len(labels)):
        temp_corr[labels[i]] = new_data[i].iloc[:,len(labels)-1]
        
    return temp_corr


def plotEconomies(labels):
    """
    Parameters
    ----------
    labels : list[str()]
        The countries to plot.
        
    Returns
    -------
        Creates a bar chart showing the changes in GDP indexed to 1995 as 
        well as showing the breakdown in the sectors contribution to GDP
    """
    fig, ax = plt.subplots()
    
    #Initialising values for later
    cols = ['Manufacturing GDP', 
            'Industry GDP', 
            'Agriculture GDP', 
            'Services GDP']
    
    colours = ['#4B0082', '#9400D3', '#999900', '#CCCC00']
    
    #set up parameters for creating the bars in the chart
    N = len(labels)
    ind = np.arange(N) 
    width = 0.25
    
    for nth, label in enumerate(labels):
        #construct dataframes for our countries
        data = [econ_m_df, econ_i_df, econ_a_df, econ_s_df, gdp_tot_df]
        columns = ['Manufacturing', 
                   'Industry', 
                   'Agriculture', 
                   'Services', 
                   'GDP']
        temp = buildDataForLabel(data, columns, label)
        
        #Multiply the sector % contribution to GDP by the total GDP and
        #divide by 100 to get the value of the sector
        temp['Manufacturing GDP'] = (temp['Manufacturing']*temp['GDP'])/100
        temp['Industry GDP'] = (temp['Industry']*temp['GDP'])/100
        temp['Agriculture GDP'] = (temp['Agriculture']*temp['GDP'])/100
        temp['Services GDP'] = (temp['Services']*temp['GDP'])/100
        
        #Get the values for the years of interest
        temp = temp.loc[['1995', '2015']]
        
        #Index the values based on the countires GDP in 1995
        indexer = temp.loc['1995', cols].sum()
        temp['Manufacturing GDP'] =  (temp['Manufacturing GDP']/indexer)*100
        temp['Industry GDP'] = (temp['Industry GDP']/indexer)*100
        temp['Agriculture GDP'] = (temp['Agriculture GDP']/indexer)*100
        temp['Services GDP'] = (temp['Services GDP']/indexer)*100
    
        #Create the bar for 1995
        bottom = 0
        for n, i in enumerate(cols):
            #stack the boxes for each sector of the economy
            ax.bar(ind[nth]-(width/2), 
                   temp[i].iloc[0], 
                   width, 
                   color = colours[n], 
                   bottom = bottom)
            bottom += temp[i].iloc[0]
            
        #Create the bar for 2015
        bottom = 0
        for n, i in enumerate(cols):
            #stack the boxes for each sector of the economy
            ax.bar(ind[nth]+(width/2), 
                   temp[i].iloc[1], 
                   width, 
                   color = colours[n], 
                   bottom = bottom)
            bottom += temp[i].iloc[1]
            
    #labels for the plot
    plt.xticks(ind, 
               labels, 
               fontsize = 'small')
    plt.title('Index of GDP Broken Down by Sector (1995 = 100)')
    plt.xlabel('Country')
    plt.ylabel('GDP')
    ax.legend(['Manufacturing', 'Industry', 'Agriculture', 'Services'],
              loc='center left', 
              bbox_to_anchor=(1, 0.75))
    
    plt.savefig('graphs/EconomiesPlot.png', bbox_inches='tight')


def plotChange(labels, df, title): 
    
    """
    Parameters
    ----------
    labels : list[str()]
        The countries to plot.
    df : pd.DataFrame
        the variable the change will be plotted for
    title : list[str()]
        The title of the plot       
    Returns
    -------
        Creates a lineplot showing how the the variable in the df dataframe 
        #has changed for the labels passed to the function between 1995 and
        #2015
    """
    fig, ax = plt.subplots()
    df = df.fillna(0)
    x = [str(year) for year in range(1995, 2016)]
    for i in labels:
        y = []
        #if we have missing data, impute the values based on the last known 
        #value
        for n, year in enumerate(x):
            if df.loc[year, i] != 0:
                y.append(df.loc[year, i])
            else:
                y.append(y[n-1])
        ax.plot(x, y, label = i)
        
    plt.legend(loc='center left', 
               bbox_to_anchor=(1, 0.75))
    plt.xticks(rotation = 45)
    plt.xlabel('Year')
    plt.ylabel('{} Index'.format(title))
    plt.title('graphs/{} Changes Between 1995 and 2015'.format(title))
    plt.savefig('graphs/CO2Plot.png', bbox_inches='tight')    


#Import the dataframes of interest
c02_df, c02_df_tr = getDfs('datasets/C02PerCapita.csv')
c02_abs_df, c02_abs_df_tr = getDfs('datasets/C02Absolute.csv')
current_df, current_df_tr = getDfs('datasets/CurrentAccount.csv')
gdp_df, gdp_df_tr = getDfs('datasets/GDPPerCapita.csv')
gdp_tot_df, gdp_tot_df_tr = getDfs('datasets/GDPTotal.csv')              
fossil_df, fossil_df_tr = getDfs('datasets/fossil.csv')
imports_df, imports_df_tr = getDfs('datasets/LowIncomeImports.csv')
urban_df, urban_df_tr = getDfs('datasets/UrbanPop.csv')
forest_df, forest_df_tr = getDfs('datasets/Forest.csv')

#import economy databases
econ_m_df, econ_m_df_tr = getDfs('economy/Manufacturing.csv')
econ_i_df, econ_i_df_tr = getDfs('economy/Industry.csv')
econ_a_df, econ_a_df_tr = getDfs('economy/Agriculture.csv')
econ_s_df, econ_s_df_tr = getDfs('economy/Services.csv')

    
#%%
#%%
#Establishing the relationship between the current account and CO2 emissions

data = [current_df_tr, c02_df_tr, gdp_df_tr] 
labels = ['Current Account', 'C02', 'GDP']
corr_df = buildDataForLabel(data, labels, 2015)

corr_df.plot.scatter('Current Account', 'C02')

fig, ax = plt.subplots()

ax.scatter(corr_df.loc[:,'Current Account'], corr_df.loc[:,'C02'], s = 1)
plt.axvline(0, color = 'black')
plt.xlabel('Current account balance (% of GDP)')
plt.ylabel('CO2 emissions (metric tons per capita)')
plt.title('Current Account Against C02 Emissions For Countries in 2015')

plt.savefig('graphs/Scatterplot.png')

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

plt.savefig('graphs/Linefig.png')


#%%

#looking at the countries that experianced the highest and lowest rates of 
#changes in CO2 emissions

c02_inv = c02_abs_df.copy()
c02_inv['change'] = (c02_inv['2015']/c02_inv['1995'] - 1)

c02_inv = c02_inv.sort_values('change')
print(c02_inv.index[:15])

c02_inv = c02_inv.sort_values('change', ascending = False)
print(c02_inv.index[:15])

fallers = ['Sweden', 'Denmark', 'France', 'United Kingdom', 'Germany']
plotEconomies(fallers)
plotChange(fallers, imports_df_tr, '% Imports from Low/Mid-Income')

risers = ['India', 'Saudi Arabia', 'Indonesia', 'Korea, Rep.', 'Brazil']
plotEconomies(risers)
plotChange(risers, imports_df_tr, 'Imports')


#%%
#Looking at changes in emissions by region

regions = ['Central Europe and the Baltics',
           'Europe & Central Asia',
           'North America',
           'Africa Western and Central',
           'Sub-Saharan Africa',
           'Africa Eastern and Southern',
           'Middle East & North Africa',
           'South Asia',
           'East Asia & Pacific',
           'World',]


temp_series = buildDataForLabel([c02_abs_df], ['CO2'], regions[0])
temp_series = temp_series.iloc[:,0].loc['1995':'2015']
temp_series = [round((temp_series[i+1]/temp_series[i] - 1)*100,2) 
               for i in range(0, len(temp_series)-1)]

index = [year for year in range(1996, 2016)]
regions_df = pd.DataFrame(temp_series, columns = [regions[0]], index = index)

for n in range(1, len(regions)):
    temp_series = buildDataForLabel([c02_abs_df], 
                                    ['CO2'], 
                                    regions[n]).iloc[:,0].loc['1995':'2015']
    temp_series = [round((temp_series[i+1]/temp_series[i] - 1)*100,2) 
                   for i in range(0, len(temp_series)-1)]
    regions_df[regions[n]] = temp_series
    
investigate = regions_df.describe()


#%%

fig, ax = plt.subplots()
x = list(c02_inv['change'].fillna(0))
x = [i*100 for i in x if i != 0]
x.sort()
x = x[:-3]
plt.plot(x, stats.norm.pdf(x, loc = np.mean(x), scale = np.std(x)))
plt.title('Distribution of Percent Change of CO2 Emissions Between 1995-2015')
plt.savefig('graphs/Ditsfig.png')

print(stats.skew(x))
print(stats.kurtosis(x))

corr_df = c02_inv[['change', '1995']] 

#%%

fig, ax = plt.subplots()

country = 'Denmark'
data = [c02_abs_df, gdp_df, fossil_df, imports_df, urban_df, forest_df] 
labels = ['C02', 
          'GDP', 
          'Fossil Fuels', 
          'Imports (Low/Mid)', 
          'Urban Population', 
          'Forest Cover']
corr_df = buildDataForLabel(data, labels, country)
ax.matshow(corr_df.corr())
plt.xticks(range(len(labels)), labels, rotation = 90)
plt.yticks(range(len(labels)), labels)
for (i, j), z in np.ndenumerate(corr_df.corr()):
    ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')
    
plt.title('{} Correlation Plot'.format(country))

plt.savefig('graphs/{}Plot.png'.format(country), bbox_inches='tight')



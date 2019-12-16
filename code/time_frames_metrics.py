############################################################################################

# This script builds a dictionary containing relevant metrics for each time interval with at
# least 7 years of observations.
# The first key of the dictionary tells you the upper bound of the time frame considered.
# Its values are a list containing all the years in the time frame and all the intervals of at 
# least seven years for the given upper bound.
# For each interval, we then store the following information:

#### Total number of indicators.
#### The list of indicators.
#### The number of missing observations.
#### The number of actual observations (i.e. before interpolation).
#### The number of total observations (i.e. after interpolation).
#### The number of SDGs covered.
#### The list of SDGs covered.
#### The number of indicators per SDG covered.
#### The number of targets per SDG covered.
#### The number of targets covered.
#### The list of targets covered.
#### The number of indicators per target covered.
#### The list of the years in the interval

# The script also retrieves the intervals with the maximum number of observations before and
# after interpolation.
# Information is based on dataset: big_sample.xlsx, test_sample_recoded.xlsx, test_sample_3_recoded.xlsx.
# Authors: Daniele Guariso
# Last update: 13/12/2019

############################################################################################

import numpy as np
import pandas as pd
import os

home =  os.getcwd()[0:-4]

df_big = pd.read_excel(home+'data\\big_sample.xlsx')
# df_big = pd.read_excel(home+'data/big_sample.xlsx')

df_indicators1 = pd.read_excel(home+'data\\test_sample_recoded.xlsx')
# df_indicators1 = pd.read_excel(home+'data/test_sample_recoded.xlsx')

df_indicators2 = pd.read_excel(home+'data\\test_sample_3_recoded.xlsx')
# df_indicators2 = pd.read_excel(home+'data/test_sample_3_recoded.xlsx')


list_indicators1 = df_indicators1['Nombre'].tolist()
list_indicators2 = df_indicators2['Name'].tolist()
list_indicators = list_indicators1 + list_indicators2

list_index = []

for index, row in df_big.iterrows():
    if row['seriesName'] in list_indicators :
        list_index.append(index)

# Select only those indicators that were recoded
        
df_subset_big = df_big.iloc[list_index].copy()

# Use new codification for targets and SDGs

df_indicators1 = df_indicators1[['Nombre', 'ODS', 'target']]
df_indicators1.rename(columns={"Nombre" : "seriesName", "ODS" : "goal"} , inplace=True)

df_indicators2 = df_indicators2[['Name', 'goal', 'target']]
df_indicators2.rename(columns={"Name" : "seriesName"} , inplace=True)

df_indicators = df_indicators1.append(df_indicators2, ignore_index= True)

df_subset_big.drop(columns=['goal', 'target'], inplace=True)

df_subset_big = df_subset_big.merge(df_indicators , on='seriesName')
                    
Years = np.arange(1990, 2018)

# Create dictionary for time frames.

dict_time_frames = {}

for i in np.arange(1, 23) :
    if i == 1 :
        dict_time_frames['time_frames_{0}'.format(Years[-i])] = {'Years' : Years}
    else :
        dict_time_frames['time_frames_{0}'.format(Years[-i])] = {'Years' : Years[:(-i+1)]}

# Store all possible time intervals of at least seven years given the upper bound.
        
for tf1 in dict_time_frames:    
    dict_time_frames[tf1]['Intervals'] = {}
    for j in range(len( dict_time_frames[tf1]['Years'])):
        if (len( dict_time_frames[tf1]['Years'][j:]) >= 7):
             dict_time_frames[tf1]['Intervals'].update({ '{0}-{1}'.format(dict_time_frames[tf1]['Years'][j],dict_time_frames[tf1]['Years'][-1]): {"years_int" : dict_time_frames[tf1]['Years'][j:]}})
        else :
            continue

# Collect relevant metrics for each interval.
            
for tf2  in dict_time_frames:  
    for interval in dict_time_frames[tf2]['Intervals'] : 
        indicators = []
        for index1, row1 in df_subset_big.iterrows():
            
        # Keep the index if obs for first and last year of the interval is not missed 
        
           if ~np.isnan(row1[str(dict_time_frames[tf2]['Intervals'][interval]['years_int'][0])]) and ~np.isnan(row1[str(dict_time_frames[tf2]['Intervals'][interval]['years_int'][-1])]) :
                indicators.append(index1)
                
        sub_df = df_subset_big.iloc[indicators].copy()
        
        targets = list(set(sub_df['target'].tolist()))
        targets_tot = len(targets)
        
        dict_time_frames[tf2]['Intervals'][interval]['Obs_Tot'] = len(indicators)*len(dict_time_frames[tf2]['Intervals'][interval]['years_int'])
        dict_time_frames[tf2]['Intervals'][interval]['Ind_Tot'] = len(indicators)
        dict_time_frames[tf2]['Intervals'][interval]['Indicators']= indicators
        dict_time_frames[tf2]['Intervals'][interval]['Targets']= targets
        dict_time_frames[tf2]['Intervals'][interval]['Targets_Tot']= targets_tot
        
        df_subset_targets = sub_df.groupby(['target']).size().reset_index(name='counts')
        dict_time_frames[tf2]['Intervals'][interval]['Target_Ind'] = {}
        
        for index2 , row2 in df_subset_targets.iterrows() :
            target_ind = {row2['target'] : row2['counts']}
            dict_time_frames[tf2]['Intervals'][interval]['Target_Ind'].update(target_ind)
            
        sdgs = list(set(sub_df['goal'].tolist()))
        sdgs_tot = len(sdgs)
        
        dict_time_frames[tf2]['Intervals'][interval]['SDGs']= sdgs
        dict_time_frames[tf2]['Intervals'][interval]['SDGs_Tot']= sdgs_tot
        
        df_subset_sdg_targets = sub_df.groupby(['goal'])['target'].nunique().reset_index(name='counts')
        dict_time_frames[tf2]['Intervals'][interval]['SDG_Target'] = {}
        
        for index3 , row3 in df_subset_sdg_targets.iterrows() :
            sdg_target = {row3['goal'] : row3['counts']}
            dict_time_frames[tf2]['Intervals'][interval]['SDG_Target'].update(sdg_target)
            
        df_subset_sdg_indicators = sub_df.groupby(['goal']).size().reset_index(name='counts')
        dict_time_frames[tf2]['Intervals'][interval]['SDG_Ind'] = {}
        
        for index4 , row4 in df_subset_sdg_indicators.iterrows() :
            sdg_ind = {row4['goal'] : row4['counts']}
            dict_time_frames[tf2]['Intervals'][interval]['SDG_Ind'].update(sdg_ind)
            
        years_list = [str(year) for year in dict_time_frames[tf2]['Intervals'][interval]['years_int']]
        missing_df = sub_df[years_list].isnull().sum().sum()
        
        dict_time_frames[tf2]['Intervals'][interval]['Missing_Tot'] = missing_df
        dict_time_frames[tf2]['Intervals'][interval]['Obs_Actual'] = len(indicators)*len(dict_time_frames[tf2]['Intervals'][interval]['years_int']) - missing_df

## Retrieve interals with max N of obs. before and after interpolation.
        
dict_max_obs = {}
for tf3  in dict_time_frames :
    for interval in dict_time_frames[tf3]['Intervals'] : 
        dict_max_obs.update({interval : dict_time_frames[tf3]['Intervals'][interval]['Obs_Tot']})

dict_max_obs_act = {}
for tf4  in dict_time_frames :
    for interval in dict_time_frames[tf4]['Intervals'] : 
        dict_max_obs_act.update({interval : dict_time_frames[tf4]['Intervals'][interval]['Obs_Actual']})

interval_max_obs = max(dict_max_obs, key=dict_max_obs.get)
interval_max_obs_act = max(dict_max_obs_act, key=dict_max_obs_act.get)
   
print('''
      The interval with the maximum number of observations (after interpolation) is {0} with {1} observations.\n
      The interval with the maximum number of observations (before interpolation) is {2} with {3} observations.\n
      The interval {0} covers {4} SDGs out of 17 and {5} targets out of 169.
      '''.format(interval_max_obs, dict_max_obs[interval_max_obs], interval_max_obs_act, dict_max_obs_act[interval_max_obs_act],
      dict_time_frames['time_frames_'+interval_max_obs[-4:]]['Intervals'][interval_max_obs]['SDGs_Tot'],
      dict_time_frames['time_frames_'+interval_max_obs[-4:]]['Intervals'][interval_max_obs]['Targets_Tot']))
    

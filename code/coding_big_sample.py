############################################################################################

# This script creates a new dataset (big_sample_recoded.xlsx) which contains the recoded 
# indicators with all the relevant information.
# Information is based on dataset: big_sample.xlsx, test_sample_recoded.xlsx, test_sample_3_recoded.xlsx.
# Authors: Daniele Guariso
# Last update: 26/12/2019

############################################################################################

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

df_subset_big.to_excel(home+'data\\big_sample_recoded.xlsx', index=False, encoding='utf-16')

# df_subset_big.to_excel(home+'data/big_sample_recoded.xlsx', index=False, encoding='utf-16')

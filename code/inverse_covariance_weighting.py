############################################################################################

# This script detrends and standardizes the indicators in the file big_sample_recoded.xlsx.
# It then computes aggregate indicators for those targets that have multiple indicators.
# The methodology applied relies on inverse covariance weighting as proposed in:

# Anderson, M.L., 2008. Multiple inference and gender differences in the effects of early 
# intervention: A reevaluation of the Abecedarian, Perry Preschool, and Early Training Projects. 
# Journal of the American statistical Association, 103(484), pp.1481-1495.

# The resulting indicators are then normalized.
# The final dataset (composite_indicators.xlsx) contains the new set of indicators (either composite
# or the original if only one indicator was available for that target), a dummy variable for the original
# indicator being constant, the target and a dummy variable to distinguish between composite and 
# original indicators.
# Information is based on dataset: big_sample_recoded.xlsx.
# Authors: Daniele Guariso
# Last update: 05/01/2020

############################################################################################


from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import os

home =  os.getcwd()[0:-4]

df = pd.read_excel(home+'data\\big_sample_recoded.xlsx')
# df = pd.read_excel(home+'data/big_sample_recoded.xlsx')

# indicators 2 and 4 are perfectly collinear, excluding N° 4.
# indicators 5 and 6 are perfectly collinear, excluding N° 6.
# indicators 12 and 16 are perfectly collinear, excluding N° 16.
# indicators 15 and 17 are perfectly collinear, excluding N° 17 as less comprehensive.
# Excluding 117 because redundant (same as 33)
# Excluding 58 as linear combination of 53 and 55.
# Excluding 69 (almost perfectly collinear with 70 and less comprehensive)
# Excluding 354 because redundant (same as 353)
# Excluding 253 because redundant (same as 251)
# Excluding 252 because redundant (same as 248)
# Excluding 259 because redundant (same as 258)
# Excluding 260 because redundant (same as 257)
# Excluding 262 because redundant (same as 263)
# Excluding 265 because redundant (same as 292)
# Excluding 308 because redundant (same as 344)
# Excluding 331 because redundant (same as 327)
# Excluding 363 because redundant (same as 359)

bad_ind = df.index.isin([4,6,16,17,58,69,117,252,253,257,259,262,265,308,331,354,363])
df = df[~bad_ind]

# Dataset should contain only the years we are interested in

# Select time interval of interest

years = np.arange(2006, 2016)
colYears = np.array([str(year) for year in years])

# Select indicators that have no missing values in the time interval of interest

list_nan_ind = list()

for index, row in df.iterrows():
    y = pd.DataFrame(row[colYears]).values
    y_list = y.tolist()
    if np.any(np.isnan(y_list)):
        list_nan_ind.append(index)

nan_ind = df.index.isin(list_nan_ind)
df = df[~nan_ind]

# Detrend the data (removing a linear trend)

df_copy = df.copy()
df_copy["constant"] = 0

for index, row in df_copy.iterrows():
    y = pd.DataFrame(row[colYears]).values
    y = y.reshape((len(y), 1)).astype(float)
    x = years.reshape((len(years), 1)).astype(float)
    linmodel = LinearRegression()
    linmodel.fit(x, y)
    trend = linmodel.predict(x)
    detrended = [y[:,0][i]-trend[:,0][i] for i in range(0, len(y))]
    df_copy.at[index,colYears]= detrended

# Standardize the data (demeaning and dividing by the sample standard deviation)
    
for index, row in df_copy.iterrows():
    if np.std(df_copy.loc[index,colYears], ddof=1) != 0:
        df_copy.at[index,colYears] = (df_copy.loc[index,colYears] - np.mean(df_copy.loc[index,colYears]))/np.std(df_copy.loc[index,colYears], ddof=1)
    else:
        df_copy.at[index,"constant"] = 1
        
# Create new dataframe with composite indicators
# Add info on weights in old dataframe
            
newdf =  pd.DataFrame(columns = colYears.tolist()+[ 'constant', 'target', 'composite_index'])
df_copy["weights"] = np.nan
for name, group in df_copy.groupby("target"):
    if group.shape[0] < 2 :
        df_group = group.copy()[colYears.tolist() + ['constant']]
        df_group.at[:,"target"] = name
        df_group.at[:,"composite_index"] = 0
        newdf = newdf.append(df_group , ignore_index=True)
    else :
        df_group = group.copy()[group.constant==0]
        if df_group.shape[0] == 1 :
            df_group = df_group[colYears.tolist() + ['constant']]
            df_group.at[:,"target"] = name
            df_group.at[:,"composite_index"] = 0
            newdf = newdf.append(df_group , ignore_index=True)
        else :
            groupT = df_group[colYears.tolist()].T
            ivec = np.asmatrix(np.ones([groupT.shape[1],1]))
            covmat = np.cov(groupT, rowvar=False)
            weights = np.linalg.inv(ivec.T @ np.linalg.inv(covmat) @ ivec) @ (ivec.T @ np.linalg.inv(covmat))
            df_copy.at[groupT.columns.values,"weights"] = np.array(weights.reshape(weights.shape[1],weights.shape[0]))[:,0].tolist()
            index = (np.linalg.inv(ivec.T @ np.linalg.inv(covmat) @ ivec) @ (ivec.T @ np.linalg.inv(covmat) @ groupT.T)).T
            dict_val = { colYears[i] : index[i,0] for i in np.arange(len(colYears))}
            dict_val["constant"] = 0
            dict_val["target"] = name
            dict_val["composite_index"] = 1
            newdf = newdf.append(dict_val, ignore_index=True)

# Indicators 10, 13 nd 14 in target 1.1 are almost perfectly collinear, consider leaving only one.
# Target 4.2 has only one indicator (202), which is constant over time, but it seems that has already reach its "maximum".
# Indicators in target 10.2 are highly correlated, consider leaving only some of them.
# Indicators 112 and 113 in target 17.12 are almost perfectly collinear, consider removing one.    
# Indicators 289 and 293 in target 17.13 are almost perfectly collinear, consider removing one. 
# Indicators 108 and 290 in target 17.13 are almost perfectly collinear, consider removing one.           
# If a target has only two indicators and one of them is constant, the composite index is effectively 
# the indicator that varies.
# Indicators 150, 152, 158, 159, 163, 164, 183, 184 in target 3.2 are almost perfectly collinear, consider leaving only a subset.
# Indicators 149, 181, 182 in target 3.3 measure the same feature (different sources), consider leaving only one.
# Indicators 141 and 173 in target 3.3 measure the same feature (different sources), consider leaving only one.
# Indicators 240 and 241 in target 5.5 measure the same feature (different sources), consider leaving only one.
# Indicators 248, 250 and 251 in target 6.2 are almost perfectly collinear, consider leaving only one.
# Indicators 291 and 292 in target 8.1 are almost perfectly collinear, consider leaving only one.
# Indicators 327, 328, 329 and 330 in target 8.5 are almost perfectly collinear, consider leaving only a subset.
# Indicators 343 and 345 in target 9.5 are almost perfectly collinear, consider leaving only one.

# Normalize the data (restrict the interval of possible values to [0,1])
        
for index, row in newdf.iterrows():
    y = pd.DataFrame(row[colYears]).values
    y_list = y.tolist()
    if np.any(np.isnan(y_list)):
        continue
    else:
        y = y.reshape((len(y), 1)).astype(float)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaler = scaler.fit(y)
        normalized = scaler.transform(y)
        newdf.at[index,colYears]= normalized[:,0].tolist()

newdf.to_excel(home+'data\\composite_indicators.xlsx', index=False, encoding='utf-16')
# newdf.to_excel(home+'data/composite_indicators.xlsx', index=False, encoding='utf-16')

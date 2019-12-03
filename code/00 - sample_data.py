import matplotlib.pyplot as plt
import numpy as np
import pickle as pk
import random as rd
import scipy.stats as st
import networkx as nx
import os, csv
import pandas as pd
import uuid, string
import scipy.optimize as opt
import copy
stamp = uuid.uuid4()


from pathlib import Path
home = str(Path.home())


years = np.arange(1990, 2018)
colYears = np.array([str(year) for year in years])

sgoals = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
          '14', '15', '16a', '16b', '17']
goal2ind = dict(zip(sgoals, range(18)))

file = open(home+"/Dropbox/Projects/ppi2_uruguay/data/color_codes.txt", 'r')
colors_sdg = dict([(sgoals[i], line[0]) for i, line in enumerate(csv.reader(file))])
file.close()


df = pd.read_csv(home+"/Dropbox/Projects/ppi2_uruguay/data/raw_complete.csv", 
                 sep='\t', low_memory=False, encoding='utf-16')
df['goal'][df.goal=='16a'] = '16'
df['goal'][df.goal=='16b'] = '16'

dfu = df[df.countryCode=='URY']
newRows = []
for intex, row in dfu.iterrows():
    obs = colYears[~np.isnan(row[colYears].values.astype(float))] 
    if len(obs) > 6:
        goal = row.goal
        if len(goal) > 2:
            goal = goal[0:2]
        newRows.append([row.seriesName, int(goal), row.target, len(obs), '-'.join(obs), np.nan, np.nan])
dfuf = pd.DataFrame(newRows, columns=['Nombre', 'ODS', 'target', 'Observaciones', 'Años', 'Importante', 'Instrumental'])
dfuf.sort_values(['ODS'], inplace=True)
dfuf.to_excel(home+"/Dropbox/Projects/ppi2_uruguay/data/test_sample.xlsx", index=False, encoding='utf-16')




info_names = pd.read_excel(home+'/Dropbox/Projects/ppi2_uruguay/data/indices_nombres.xlsx')
#df = df[np.in1d(df.seriesCode, info_names.seriesCode)]
df = df[(df.seriesCode != 'EOSQ146') & (df.seriesCode != 'CC.EST') & (df.seriesCode != 'RL.EST')]


new_rows = []
conevals = [col for col in df.seriesCode.unique() if 'coneval' in col]
for code, group in df.groupby('seriesCode'):
    print(code)
    
    V = group.values
    M = V[:,0:28].astype(float)
    values = np.array(M[~np.isnan(M)])

    if code not in ['TASA.INF']+conevals:
        if len(set(values)) > 1:
            values = (values - values.min())/(values.max() - values.min())
        else:
            values[:] = 1
        
    if code in conevals:
        values /= 100
        
    if group.reverse.values[0] == 1:
        print(33)
        values = np.abs(values-1)
            
    
    V[:,0:28][~np.isnan(M)] = values
    new_rows += V.tolist()


dfn = pd.DataFrame(new_rows, columns=df.columns)
dfn.sort_values(['goal', 'seriesCode'], inplace=True)
dfn.to_csv(home+"/Dropbox/Projects/ppi2_uruguay/data/norm_complete.csv", index=False, sep='\t', encoding='utf-16')

dfn = dfn[dfn.countryCode=='URY']
dfn.reset_index(inplace=True)
dfn.drop(columns=['index'], inplace=True)
dfn.sort_values(['goal', 'seriesCode'], inplace=True)


## Interpolate missing observations
newRows = []
for index, row in dfn.iterrows():
    serie = row[colYears].values.astype(float)
    info = np.where(~np.isnan(serie))[0]
    if len(info) > 1:
        for i in range(len(info)-1):
            ss = serie[info[0]:info[-1]+1]
            yy = years[info[0]:info[-1]+1]
            interData = np.interp(yy[np.isnan(ss)], years[info], serie[info])
            serie[info[0]+np.where(np.isnan(ss))[0]] = interData
    newRows.append(serie.tolist() + row[df.columns.values[28::].tolist()].values.tolist())
dff = pd.DataFrame(newRows, columns=dfn.columns)

dff = dff[(~np.isnan(dff[colYears].values)).sum(axis=1)>6]

ins = pd.read_excel(home+'/Dropbox/Projects/ppi2_uruguay/data/test_sample_Uruguay_SPG_VNR.xls')


not_in = list((set(dff.seriesName) - set(ins.Nombre)))
dfuf2 = pd.DataFrame(dff[np.in1d(dff.seriesName, not_in)][['seriesName', 'goal']].values, columns=['Nombre', 'ODS'])
dfuf2.sort_values(['ODS'], inplace=True)
dfuf2['Sistema de Planificación General'] = np.nan
dfuf2['VNR'] = np.nan
dfuf2.to_excel(home+"/Dropbox/Projects/ppi2_uruguay/data/test_sample_2.xlsx", index=False, encoding='utf-16')



not_in = list((set(dff.seriesName) - set(ins.Nombre)))
dfuf2 = pd.DataFrame(dff[np.in1d(dff.seriesName, not_in)][['seriesName', 'seriesCode', 'goal', 'target']].values, columns=['Name', 'seriesCode', 'goal', 'target'])
dfuf2.sort_values(['goal'], inplace=True)
dfuf2.to_excel(home+"/Dropbox/Projects/ppi2_uruguay/data/test_sample_3.xlsx", index=False, encoding='utf-16')




### Attempt to assemble series


for year1 in range(2000, 2012):
    for year2 in range(year1+6, 2018):
        clyrs = [str(y) for y in range(year1, year2)]
        M = dff[clyrs].values
        dfff = dff.iloc[np.where(np.isnan(M).sum(axis=1)==0)[0]]
        if year2==2017:
            print(len(dfff.goal.unique()), len(dfff), year1, year2)
        




#sample_years = np.arange(2006, 2017)
#sample_colYears = [str(year) for year in sample_years]
#
#dff
#
#dff = dff[sample_colYears + df.columns[28::].tolist()]
#dfr = df[sample_colYears + df.columns[28::].tolist()]
#dfr = dfr[dfr.countryCode=='URY']
#
## Filter those without missing observations
#preserve = ~np.isnan(dff[sample_colYears].values.sum(axis=1))
#dff = dff[preserve]
#dfr = dfr[preserve]


#dff['goals'] = copy.deepcopy(dff.goal.values)
#dff['goals'][dff.goal=='17'] = '18'
#dff['goals'][dff.goal=='16a'] = '16'
#dff['goals'][dff.goal=='16b'] = '17'
#dff['goals'] = pd.to_numeric(dff['goals'])
#dff.sort_values(['goals', 'seriesCode'], inplace=True)
#dff.drop(columns='goals', inplace=True)
#
#dfr['goals'] = copy.deepcopy(dfr.goal.values)
#dfr['goals'][dfr.goal=='17'] = '18'
#dfr['goals'][dfr.goal=='16a'] = '16'
#dfr['goals'][dfr.goal=='16b'] = '17'
#dfr['goals'] = pd.to_numeric(dfr['goals'])
#dfr.sort_values(['goals', 'seriesCode'], inplace=True)
#dfr.drop(columns='goals', inplace=True)
#
#dff = dff.drop('source', 1)
#dfr = dfr.drop('source', 1)
#
#dff = dff.drop('non-redundant', 1)
#dfr = dfr.drop('non-redundant', 1)
#
#dff['goalOfficial'] = copy.deepcopy(dff['goal'])
#dff['goalOfficial'][dff.goalOfficial=='16a'] = '16'
#dff['goalOfficial'][dff.goalOfficial=='16b'] = '16'
#
#dff['goalColor'] = [colors_sdg[goal] for goal in dff.goal.values]
#dff['goalColorOfficial'] = [colors_sdg[goal] if goal != '16' else colors_sdg['16a'] for goal in dff.goalOfficial.values]
#
#dfr['goalOfficial'] = copy.deepcopy(dfr['goal'])
#dfr['goalOfficial'][dfr.goalOfficial=='16a'] = '16'
#dfr['goalOfficial'][dfr.goalOfficial=='16b'] = '16'
#
#dfr['goalColor'] = [colors_sdg[goal] for goal in dfr.goal.values]
#dfr['goalColorOfficial'] = [colors_sdg[goal] if goal != '16' else colors_sdg['16a'] for goal in dfr.goalOfficial.values]



#dff.to_csv(home+"/Dropbox/Projects/ppi2_uruguay/data/final_sample_normalized.csv", index=False, sep='\t', encoding='utf-16')
#dfr.to_csv(home+"/Dropbox/Projects/ppi2_uruguay/data/final_sample_raw.csv", index=False, sep='\t', encoding='utf-16')









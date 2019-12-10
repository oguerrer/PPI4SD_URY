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
stamp = uuid.uuid4()


from pathlib import Path
home = str(Path.home())


years = np.arange(1990, 2018)
colYears = np.array([str(year) for year in years])

home =  os.getcwd()[0:-4]


df = pd.read_csv(home+"data/raw_complete.csv", 
                 sep='\t', low_memory=False, encoding='utf-16')
df['goal'][df.goal=='16a'] = '16'
df['goal'][df.goal=='16b'] = '16'

dfu = df[df.countryCode=='URY']
dfu.to_excel(home+"data/big_sample.xlsx", index=False, encoding='utf-16')





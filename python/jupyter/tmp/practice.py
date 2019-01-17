#!/usr/bin/env pypthon3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


d1 = {'dates':['20170101','20170101','20170102'], 'output':[100,100,300]}
d2 = {'dates':['20170101','20170101','20170102'], 'output':[200,200,400]}
d3 = {'dates':['20170101','20170102'], 'output':[500,600]}
df1 = pd.DataFrame(data=d1)
df2 = pd.DataFrame(data=d2)
df3 = pd.DataFrame(data=d3)
df1 = df1.drop_duplicates()
df2 = df2.drop_duplicates()

df = pd.merge(df1, df2, on='dates')
df = pd.merge(df, df3, on='dates')
print(df)

for i in df.drop('dates', axis=1):
    print(df[i])


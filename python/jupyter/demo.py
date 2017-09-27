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
print(df1)
print(df2)
print(df3)

df = pd.merge(df1, df2, on='dates')
print(df)
df = pd.merge(df, df3, on='dates')
print(df)

df = df.T
print(df)
for d in df.iterrows():
    print(d)


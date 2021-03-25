import os
import sys
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def get_dfs(df):
    result = []
    for id in (1,2,3,4,5,18,19):
        condition = (df['DeviceID'] == id)
        invdf = df[condition]
        invdf = invdf[['ACOutputPower']]
        
        invdfh = invdf.groupby('minute').mean()
        invdfh = invdfh.rename(columns={'ACOutputPower': 'power-{}'.format(id)})
        result.append(invdfh)
    df = pd.concat(result, axis=1)
    return df


def corr(fullpath):

    with sqlite3.connect(fullpath) as con:
        df = pd.read_sql('''SELECT * FROM inverter_minutely''', con=con)

    df.LoggedDatetime = pd.to_datetime(df.LoggedDatetime)
    df['minute'] = df.LoggedDatetime.dt.strftime('%Y-%m-%d %H:%M:00')
    df = df[['DeviceID', 'minute', 'ACOutputPower']]
    df.set_index(['minute'], inplace=True)

    df = get_dfs(df)
    df = df.dropna()
    print(df)


    df.index = pd.DatetimeIndex(df.index)
    df2 = df.resample('1H').mean()
    df3 = df2.corr()
    result = df3.mean().sort_values()
    return result 





if __name__ == '__main__':
    ret = corr('../data/demo_2020_0505.sqlite')
    print(ret)
    print(type(ret))


    for k, v in ret.items():
        print('{}: {}'.format(k, v))

    
    
    





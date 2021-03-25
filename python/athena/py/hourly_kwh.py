import os
import sys
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def get_minutely_df(fullpath):
    with sqlite3.connect(fullpath) as con:
        df = pd.read_sql('''select * from inverter_minutely''', con=con)
    df.LoggedDatetime = pd.to_datetime(df.LoggedDatetime)
    df = df.set_index('LoggedDatetime')
    return df

def split_df_with_inverters(df):
    dfs = {}
    for id in (1,2,3,4,5,18,19):
        dfs[id] = df.query('DeviceID == {}'.format(id))
    return dfs 
    

def get_inv_mean(date_str, id, dfs):
    data = []
    for h in range(5, 18):  
        start = '{} {:02d}:00:00'.format(date_str, h)
        end   = '{} {:02d}:00:00'.format(date_str, h+1)
        hourly = dfs[id][start:end] # query rows by hour
        colname = 'mean-{}'.format(id)
        d = {'hour': h, colname: hourly.ACOutputPower.mean()}
        data.append(d)
    df = pd.DataFrame(data)
    df = df.set_index('hour')
    return df


def get_all_inv_mean(date_str, dfs):
    #result = [get_inv_mean(date_str, id, dfs) for id in (1,2,3,4,5,18,19)]
    result = []
    for id in (1,2,3,4,5,18,19):
        df = get_inv_mean(date_str, id, dfs)
        result.append(df)

    result = pd.concat(result, axis=1)
    return result


def get_output_fullpath(fullpath):
    filename = os.path.split(fullpath)[-1] 
    newfilename = os.path.splitext(filename)[0] + '.png'
    outputpath = 'output/'
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    output_fullpath = outputpath + newfilename
    return output_fullpath 


def get_date(fullpath):
    filename = os.path.split(fullpath)[-1] 
    filename = os.path.splitext(filename)[0]
    year  = filename[5:9]
    month = filename[10:12]
    day   = filename[12:14]
    date = '{}-{}-{}'.format(year, month, day)
    return date 





def output_hourly_kwh(fullpath):

    df = get_minutely_df(fullpath)

    dfs = split_df_with_inverters(df)

    date = get_date(fullpath)

    mean_df = get_all_inv_mean(date, dfs)


    output_fullpath = get_output_fullpath(fullpath)
    print(output_fullpath)
    

    ax = mean_df.plot(kind='bar')
    ax.set_title(fullpath)
    #plt.show()

    ax.figure.savefig(output_fullpath)
    plt.close('all')
    return output_fullpath


def get_hourly_kwh(filename):
    dfs = {}
    for id in (1,2,3,4,5,18,19):
        cname = 'GenKWH-{}'.format(id)
        print(cname)
        with sqlite3.connect(filename) as con:
            sql = '''SELECT 
                         strftime("%H", LoggedDatetime) AS hour,  
                         (MAX(KWH) - MIN(KWH)) AS GenKWH
                     FROM 
                         inverter_minutely 
                     WHERE
                         DeviceID == (?)
                     GROUP BY hour;'''
            invdf  = pd.read_sql(sql, con=con, params=(id,))
            invdf = invdf.rename(columns={'GenKWH': 'GenKWH-{}'.format(id)})
            
            invdf = invdf.set_index('hour')
        dfs[id] = invdf
    dfs = pd.concat(dfs.values(), axis=1)
    return dfs

if __name__ == '__main__':

    '''filenames = os.listdir('../data')
    for filename in filenames:
        if filename.endswith('sqlite'):
            fullpath = '../data/{}'.format(filename) 
            ret = output_hourly_acoutputpower_bar(fullpath)
            print(ret)
            '''
            
            
            
            
            
    fullpath = '../data/demo_2020_0505.sqlite'
    ret = get_hourly_kwh(fullpath)
    print(ret)
    
    
    ax = ret.plot(kind='bar')
    ax.set_title(fullpath)
    plt.show()

    #ax.figure.savefig(output_fullpath)
    plt.close('all')
    
    
    





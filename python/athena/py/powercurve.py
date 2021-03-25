import os
import sys
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def draw_acoutputpower_curve(fullpath):

    with sqlite3.connect(fullpath) as con:
        df = pd.read_sql('''select * from inverter_minutely''', con=con)

    df.LoggedDatetime = pd.to_datetime(df.LoggedDatetime)

    fig, ax = plt.subplots(1)

    dfs = {}
    device_identifies = [1,2,3,4,5,18,19]
    for id in device_identifies:
        cmd = 'DeviceID == {}'.format(id)
        dfs[id] = df.query(cmd)

    for id in device_identifies:
        df = dfs.get(id)
        ax.plot(df.LoggedDatetime, df.ACOutputPower)

    ax.set_title(fullpath)


    filename = os.path.split(fullpath)[-1] 
    newfilename = os.path.splitext(filename)[0] + '.png'

    outputpath = 'output/'
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    full_output_path = outputpath + newfilename
    print(full_output_path )

    fig.savefig(full_output_path)
    plt.close('all')
    return full_output_path 



if __name__ == '__main__':

    filenames = os.listdir('../data')
    for filename in filenames:
        if filename.endswith('sqlite'):
            fullpath = '../data/{}'.format(filename) 
            ret = draw_acoutputpower_curve(fullpath)
            print(ret)
            
            
            
            
    '''ret = draw_acoutputpower_curve('../data/demo_2020_0505.sqlite')
    print(ret)
    '''
    
    
    





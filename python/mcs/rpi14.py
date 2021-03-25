#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import json
import time

deviceId = 'Dzr7tc0p'
deviceKey = 'LCKr4FaINiTODU0h'

'''
jupyter tips:

%pylab inline
import pandas as pd
df = pd.read_csv('~/democode/python/mcs/mcs.log')
temp = df.iloc[0:200,1]
plot(temp)
'''

if __name__ == '__main__':
    


    # 讀取資料點
    print('Get data from {}'.format(deviceId))
    headers={'DeviceKey': deviceKey, 'Content-Type':'text/csv'}
    deviceChn = '1'
    #start_ms = round((time.time()-(60*60*24*2)) * 1000)
    #end_ms = round(time.time() * 1000)
    #params = '?start={}&end={}&limit={}'.format(start_ms, end_ms, 999)
    #tmp = '?start={}&end={}'.format(round(time.time()-172800), round(time.time()))
    #print(tmp)
    #params = '?start=1490692037995&end=1490756686995&limit=5'
    params = '?limit=900'
    #print(params)
    url = 'https://api.mediatek.com/mcs/v2/devices/{}/datachannels/{}/datapoints.csv{}'.format(
        deviceId, 
        deviceChn,
        params)
    resp = requests.get(url, headers=headers)
    print(resp.text)

    records = []
    s = resp.text
    lines = s.split('\n')
    for line in lines:
        fields = line.split(',')
        chan = fields[0]
        ts = fields[1]
        temp = fields[2]
        ts = int(ts)//1000
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
        r = '{},{}'.format(timestamp, temp)
        records.append(r)
        #print(r)

    print(records)
    with open('mcs.log', 'w') as fw:
        for r in records:
            #print(r)
            fw.write(r + '\n')
        print('loop finish')
    
        

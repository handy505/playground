#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import json
import time

deviceId = 'DoDRf1I3'
deviceKey = 'LThU2YXaK8RETiXd'

if __name__ == '__main__':
    
    '''# 向server拿長連接的ip:port
    print('-------- get TCP long link ip/port')
    url = 'https://api.mediatek.com/mcs/v2/devices/{}/connections.csv'.format(
        deviceId)
    headers={'DeviceKey': deviceKey, 'Content-Type':'text/csv'}
    resp = requests.get(url, headers=headers)
    print(resp.text)'''


    # 維持長連接，未實做
    # ...


    '''# 上傳資料點
    print('-------- post data')
    url = 'https://api.mediatek.com/mcs/v2/devices/{}/datapoints.csv'.format(
        deviceId)
    rest = requests.post(url, data='1,,33.34', headers=headers)
    print(resp.text)'''


    # 讀取資料點
    print('-------- get data')
    headers={'DeviceKey': deviceKey, 'Content-Type':'text/csv'}
    deviceChn = '1'
    start_ms = round((time.time()-(60*60*24*2)) * 1000)
    end_ms = round(time.time() * 1000)
    params = '?start={}&end={}&limit={}'.format(start_ms, end_ms, 999)
    #tmp = '?start={}&end={}'.format(round(time.time()-172800), round(time.time()))
    #print(tmp)
    #params = '?start=1490692037995&end=1490756686995&limit=5'
    #params = '?limit=999'
    #print(params)
    url = 'https://api.mediatek.com/mcs/v2/devices/{}/datachannels/{}/datapoints.csv{}'.format(
        deviceId, 
        deviceChn,
        params)
    resp = requests.get(url, headers=headers)
    print(resp.text)


    '''# 讀取裝置資訊
    print('--------- get device information')
    url = 'https://api.mediatek.com/mcs/v2/devices/{}'.format(
        deviceId
    )
    headers={'DeviceKey': deviceKey, 'Content-Type':'application/json'}
    resp = requests.get(url, headers=headers)
    #print(resp.text)
    d = json.loads(resp.text)
    print(d)
    s = json.dumps(d, indent=4)
    print(s)'''

    # 回報裝置韌體版本 (400 Bad Request / 404 Not Found)
    '''print('report firmware version')
    url = 'https://api.mediatek.com/mcs/v2/devices/{}/firmwares'.format(
        deviceId
    )
    headers={'DeviceKey': deviceKey, 'Content-Type':'application/json'}
    payload = {'version': 'v1'}
    s = json.dumps(payload)
    print(s)
    
    resp = requests.put(url, headers=headers, data=json.dumps(payload))
    print(resp.text)'''

    print(time.time())
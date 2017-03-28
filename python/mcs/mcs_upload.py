#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen
import requests


deviceId = 'DoDRf1I3'
deviceKey = 'LThU2YXaK8RETiXd'

if __name__ == '__main__':

    # 向server拿長連接的ip:port
    url = 'https://api.mediatek.com/mcs/v2/devices/{}/connections.csv'.format(deviceId)
    headers={'DeviceKey': deviceKey, 'Content-Type':'text/csv'}
    resp = requests.get(url, headers=headers)
    print(resp.text)


    # 維持長連接，未實做
    # ...


    # 上傳資料點
    url = 'https://api.mediatek.com/mcs/v2/devices/{}/datapoints.csv'.format(deviceId)
    r = requests.post(url, data='1,,33.34', headers=headers)
    print(r.text)


    # 讀取資料點
    deviceChn = '1'
    url = 'https://api.mediatek.com/mcs/v2/devices/{}/datachannels/{}/datapoints.csv'.format(deviceId, deviceChn)
    resp = requests.get(url, headers=headers)
    print(resp.text)

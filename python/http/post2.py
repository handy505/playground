#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import json


'''
1) 參考 https://docs.python.org/3/library/http.client.html
2) 使用 posttestserver.com 提供的服務做驗証
'''

poststr = """
InverterData@[{"UniqueID": "40337", "InverterID": "1", "Expr1002": "2016-10-21 10:48:38", "OutputPower": "120", "ACVolPhaseA": "119", "ACVolPhaseB": "120", "ACVolPhaseC": "112", "ACFrequency": "114", "ACOutputCurrentA": "103", "ACOutputCurrentB": "108", "ACOutputCurrentC": "105", "DC1InputVol": "119", "DC2InputVol": "118", "DC1InputCurrent": "111", "DC2InputCurrent": "100", "DCBusPositiveVol": "101", "DCBusNegativeVol": "100", "InternalTemper": "119", "HeatSinkTemper": "100", "InputPowerA": "115", "InputPowerB": "113", "TotalOutputPower": "4207"}]
"""

#url = "http://posttestserver.com/post.php"
url = "http://solar.ablerex.com.tw/DataStorage/DataStorage.ashx?psid=290"
#url = 'http://httpbin.org/post'

#payload = {"name": "handy"}
#r = requests.post(url, data=json.dumps(payload))

r = requests.post(url, data=poststr)
print(r.text)
print(r.status_code)


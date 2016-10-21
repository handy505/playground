#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import http.client, urllib.parse

'''
1) 參考 https://docs.python.org/3/library/http.client.html
2) 使用 posttestserver.com 提供的服務做驗証
'''

url = "http://posttestserver.com/post.php"
poststr = """
InverterData@[{"UniqueID": "40337", "InverterID": "1", "Expr1002": "2016-10-21 10:48:38", "OutputPower": "120", "ACVolPhaseA": "119", "ACVolPhaseB": "120", "ACVolPhaseC": "112", "ACFrequency": "114", "ACOutputCurrentA": "103", "ACOutputCurrentB": "108", "ACOutputCurrentC": "105", "DC1InputVol": "119", "DC2InputVol": "118", "DC1InputCurrent": "111", "DC2InputCurrent": "100", "DCBusPositiveVol": "101", "DCBusNegativeVol": "100", "InternalTemper": "119", "HeatSinkTemper": "100", "InputPowerA": "115", "InputPowerB": "113", "TotalOutputPower": "4207"}]
"""

params = urllib.parse.urlencode({"ID1":"username", "id2":"hello"})
params = params.encode('UTF-8')
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = http.client.HTTPConnection("posttestserver.com")
#conn = http.client.HTTPConnection("solar.ablerex.com.tw")
#conn.request("POST", "", params, headers)
#conn.request("POST", "/post.php", params)
#conn.request("POST", "/post.php", s)
#conn.request("POST", "/DataStorage/DataStorage.ashx?psid=290", s, headers)
conn.request("POST", "/post.php", s, headers)
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
print(data)
print(response.__dict__)
conn.close()

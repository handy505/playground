#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from urllib import request, parse
'''
1) 參考 https://docs.python.org/3/library/http.client.html
2) 使用 posttestserver.com 提供的服務做驗証
'''

u = request.urlopen("http://solar.ablerex.com.tw/DataStorage/Info.ashx?mac=5cf9dd48e7ef")
print(u.read())


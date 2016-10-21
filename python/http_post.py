#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import http.client, urllib.parse

'''
1) 參考 https://docs.python.org/3/library/http.client.html
2) 使用 posttestserver.com 提供的服務做驗証
'''
params = urllib.parse.urlencode({"ID1":"username", "id2":"hello"})
params = params.encode('UTF-8')
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = http.client.HTTPConnection("posttestserver.com")
#conn.request("POST", "", params, headers)
conn.request("POST", "/post.php", params)
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
print(data)
conn.close()

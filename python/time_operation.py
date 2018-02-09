#!/usr/bin/env python3

import time

t = time.time()
print(t)
#1501743135.658256

ts = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(t))
print(ts)
#2017/08/03 14:52:15

struct_time = time.strptime(ts, '%Y/%m/%d %H:%M:%S')
sec = time.mktime(struct_time)
print(sec)
#1501743135.0

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time


if __name__ == "__main__":

    # timestamp
    now = time.time()
    print("now in seconds: " + str(now))

    timearr = time.localtime(now)
    print("hour: {0}, minute: {1}, seconds: {2}".format(timearr.tm_hour, 
                                                        timearr.tm_min, 
                                                        timearr.tm_sec))

'''
pi@raspberrypi:~/demo/python/lessons $ python3 04_timestamp.py 
now in seconds: 1595227382.8171701
hour: 14, minute: 43, seconds: 2
'''

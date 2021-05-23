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
now in seconds: 1621751381.8278215
hour: 23, minute: 29, seconds: 41
'''

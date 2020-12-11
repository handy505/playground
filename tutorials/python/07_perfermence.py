#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import math

def main():

    # perfermence
    t1 = time.clock()
    ans = math.sqrt(2)
    t2 = time.clock()
    print("sqrt(2) = {0}, elapse time: {1}".format(ans, t2-t1))

if __name__ == "__main__":
    main()

'''
pi@raspberrypi:~/demo/python/lessons $ python3 07_perfermence.py 
sqrt(2) = 1.4142135623730951, elapse time: 9.100000000000774e-05
'''

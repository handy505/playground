#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def add(arg1, arg2):
    return arg1 + arg2


if __name__ == "__main__":
    ret = add(2, 3)
    print('result: {}'.format(ret))


'''
pi@raspberrypi:~/demo/python/lessons $ python3 02_function_call.py 
result: 5
'''

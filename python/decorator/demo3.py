#!/usr/bin/env python3
import functools


def unit(fn, multiple):
    @functools.wraps(fn)
    def wrapper():
        return fn() * multiple 
    return wrapper 


def getvalue():
    return 100


if __name__ == '__main__':
    getvalue = unit(getvalue, 0.01)
    print(getvalue())
    print(getvalue.__name__)

'''
$ python3 demo3.py 
1.0
getvalue

'''
